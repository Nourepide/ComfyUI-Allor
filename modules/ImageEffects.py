import cv2
import numpy as np
import torch
import torchvision.transforms.functional as F

from .Utils import radialspace_1D, radialspace_2D, cv2_layer


class ImageEffectsAdjustment:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "brightness": ("FLOAT", {
                    "default": 1.0,
                    "step": 0.01
                }),
                "contrast": ("FLOAT", {
                    "default": 1.0,
                    "step": 0.01
                }),
                "saturation": ("FLOAT", {
                    "default": 1.0,
                    "step": 0.01
                }),
                "hue": ("FLOAT", {
                    "default": 0.5,
                    "max": 1.0,
                    "step": 0.01
                }),
                "gamma": ("FLOAT", {
                    "default": 1.0,
                    "step": 0.01
                }),
                "sharpness": ("FLOAT", {
                    "default": 1.0,
                    "step": 0.01
                }),
                "red": ("FLOAT", {
                    "default": 1.0,
                    "step": 0.01
                }),
                "green": ("FLOAT", {
                    "default": 1.0,
                    "step": 0.01
                }),
                "blue": ("FLOAT", {
                    "default": 1.0,
                    "step": 0.01
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/effects"

    def node(self, images, brightness, contrast, saturation, hue, gamma, sharpness, red, green, blue):
        # noinspection PyUnboundLocalVariable
        def apply(img):
            rgba = False

            if len(img[0, 0, :]) == 4:
                a = img[:, :, 3].unsqueeze(2)
                img = img[:, :, 0:3]
                rgba = True

            img = img.permute(2, 0, 1)

            if brightness != 1.0:
                img = F.adjust_brightness(img, brightness)

            if contrast != 1.0:
                img = F.adjust_contrast(img, contrast)

            if saturation != 1.0:
                img = F.adjust_saturation(img, saturation)

            if hue != 0.5:
                img = F.adjust_hue(img, hue - 0.5)

            if gamma != 1.0:
                img = F.adjust_gamma(img, gamma)

            if sharpness != 1.0:
                img = F.adjust_sharpness(img, sharpness)

            img = img.permute(1, 2, 0)

            r, g, b = torch.chunk(img, 3, dim=2)

            r = torch.clamp(r * red, 0, 1)
            g = torch.clamp(g * green, 0, 1)
            b = torch.clamp(b * blue, 0, 1)

            if rgba:
                return torch.cat([r, g, b, a], dim=2)
            else:
                return torch.cat([r, g, b], dim=2)

        return (torch.stack([
            apply(images[i]) for i in range(len(images))
        ]),)


class ImageEffectsGrayscale:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/effects"

    def node(self, images):
        def apply(image):
            tensor = image.clone().detach()
            grayscale_tensor = torch.mean(tensor, dim=2, keepdim=True)

            return torch.cat([grayscale_tensor] * 3, dim=2)

        return (torch.stack([
            apply(images[i]) for i in range(len(images))
        ]),)


class ImageEffectsNegative:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/effects"

    def node(self, images):
        tensor = images.clone().detach()
        tensor[:, :, :, 0:3] = 1.0 - tensor[:, :, :, 0:3]

        return (tensor,)


class ImageEffectsSepia:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/effects"

    def node(self, images):
        tensor = images.clone().detach()

        sepia_mask = torch.tensor([[0.393, 0.349, 0.272],
                                   [0.769, 0.686, 0.534],
                                   [0.189, 0.168, 0.131]])

        tensor[:, :, :, 0:3] = torch.stack([
            torch.matmul(tensor[i, :, :, 0:3], sepia_mask) for i in range(len(tensor))
        ])

        return (tensor,)


class ImageEffectsLensZoomBurst:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "scale": ("FLOAT", {
                    "default": 1.5,
                    "min": 1.0,
                    "step": 0.01
                }),
                "samples": ("INT", {
                    "default": 100,
                    "min": 1,
                }),
                "position_x": ("FLOAT", {
                    "default": 0.5,
                    "max": 1.0,
                    "step": 0.01
                }),
                "position_y": ("FLOAT", {
                    "default": 0.5,
                    "max": 1.0,
                    "step": 0.01
                }),
                "rotation": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 360.0,
                }),
                "method": (["circle", "point"],),
                "stabilization": (["true", "false"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/effects/lens"

    # noinspection PyUnresolvedReferences
    def zoom_burst(
            self,
            image,
            scale,
            samples,
            position,
            rotation,
            method,
            stabilization,
    ):
        if scale < 1.0:
            raise ValueError("Parameter scale can't be smaller then initial image size.")

        h, w = image.shape[:2]

        x = np.arange(w)
        y = np.arange(h)

        xx, yy = np.meshgrid(x, y)

        cx = int(w * position[0])
        cy = int(h * position[1])

        if method == "circle":
            d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
            max_d = np.sqrt((w / 2) ** 2 + (h / 2) ** 2)

            map_x_up = (xx - d * (scale - 1.0) / max_d * (xx - cx) / samples).astype(np.float32)
            map_y_up = (yy - d * (scale - 1.0) / max_d * (yy - cy) / samples).astype(np.float32)

            map_x_down = (xx + d * (scale - 1.0) / max_d * (xx - cx) / samples).astype(np.float32)
            map_y_down = (yy + d * (scale - 1.0) / max_d * (yy - cy) / samples).astype(np.float32)
        elif method == "point":
            map_x_up = (xx - (xx - cx) * (scale - 1.0) / samples).astype(np.float32)
            map_y_up = (yy - (yy - cy) * (scale - 1.0) / samples).astype(np.float32)

            map_x_down = (xx + (xx - cx) * (scale - 1.0) / samples).astype(np.float32)
            map_y_down = (yy + (yy - cy) * (scale - 1.0) / samples).astype(np.float32)
        else:
            raise ValueError("Unsupported method.")

        if rotation > 0.0:
            angle_step = rotation / samples

            rm_up = cv2.getRotationMatrix2D((cx, cy), angle_step, 1)
            rm_down = cv2.getRotationMatrix2D((cx, cy), -angle_step, 1)
        else:
            vibration_angle = 1.0
            vibration_step = vibration_angle / samples

            rm_up_even = cv2.getRotationMatrix2D((cx, cy), vibration_step, 1)
            rm_down_even = cv2.getRotationMatrix2D((cx, cy), -vibration_step, 1)

            rm_up_odd = cv2.getRotationMatrix2D((cx, cy), -vibration_step, 1)
            rm_down_odd = cv2.getRotationMatrix2D((cx, cy), vibration_step, 1)

        for i in range(samples):
            if stabilization:
                tmp_up = cv2.remap(image, map_x_up, map_y_up, cv2.INTER_LINEAR)
                tmp_down = cv2.remap(image, map_x_down, map_y_down, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

                if rotation > 0.0:
                    tmp_up = cv2.warpAffine(tmp_up, rm_up, (w, h), borderMode=cv2.BORDER_REFLECT)
                    tmp_down = cv2.warpAffine(tmp_down, rm_down, (w, h), borderMode=cv2.BORDER_REFLECT)
                else:
                    if i % 2 == 0:
                        tmp_up = cv2.warpAffine(tmp_up, rm_up_even, (w, h), borderMode=cv2.BORDER_REFLECT)
                        tmp_down = cv2.warpAffine(tmp_down, rm_down_even, (w, h), borderMode=cv2.BORDER_REFLECT)
                    else:
                        tmp_up = cv2.warpAffine(tmp_up, rm_up_odd, (w, h), borderMode=cv2.BORDER_REFLECT)
                        tmp_down = cv2.warpAffine(tmp_down, rm_down_odd, (w, h), borderMode=cv2.BORDER_REFLECT)

                image = cv2.addWeighted(tmp_up, 0.5, tmp_down, 0.5, 0)
            else:
                tmp = cv2.remap(image, map_x_up, map_y_up, cv2.INTER_LINEAR)

                if rotation > 0.0:
                    rm = cv2.getRotationMatrix2D((cx, cy), angle_step, 1)
                    tmp = cv2.warpAffine(tmp, rm, (w, h), borderMode=cv2.BORDER_REFLECT)
                else:
                    if i % 2 == 0:
                        tmp = cv2.warpAffine(tmp, rm_up_even, (w, h), borderMode=cv2.BORDER_REFLECT)
                    else:
                        tmp = cv2.warpAffine(tmp, rm_up_odd, (w, h), borderMode=cv2.BORDER_REFLECT)

                image = cv2.addWeighted(tmp, 0.5, image, 0.5, 0)

        return image

    def node(self, images, scale, samples, position_x, position_y, rotation, method, stabilization):
        tensor = images.clone().detach()

        return (cv2_layer(tensor, lambda x: self.zoom_burst(
            x, scale, samples, (position_x, position_y), rotation, method, True if stabilization == "true" else False
        )),)


class ImageEffectsLensChromaticAberration:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "shift": ("INT", {
                    "default": 10,
                    "step": 1,
                }),
                "method": (["reflect", "edge", "constant"],),
                "shift_type": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4,
                    "step": 1,
                }),
                "mixing_type": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4,
                    "step": 1,
                }),
                "transpose": (["none", "rotate", "reflect"],),
                "colors": (["rb", "rg", "gb"],),
                "lens_curvy": ("FLOAT", {
                    "default": 1.0,
                    "max": 15.0,
                    "step": 0.1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/effects/lens"

    def node(self, images, shift, method, shift_type, mixing_type, transpose, colors, lens_curvy):
        # noinspection PyUnboundLocalVariable
        def apply(image):
            img = image.clone().detach()

            if transpose == "rotate":
                img = img.permute(1, 0, 2)
            elif transpose == "none" or transpose == "reflect":
                pass
            else:
                raise ValueError("Not existing reverse.")

            r, g, b = img[:, :, 0:3].split(1, 2)
            height, width = img[:, :, 0].shape

            def get_space(size, min_val, max_val):
                size += shift * 2

                if min_val == max_val:
                    return torch.linspace(min_val, max_val, size)
                else:
                    return radialspace_1D(size, lens_curvy, 1.0, min_val, max_val)

            if shift_type == 1:
                f_shifts = get_space(height, -shift, shift)

                if transpose == "reflect":
                    t_shifts = get_space(width, -shift, shift)
            elif shift_type == 2:
                f_shifts = get_space(height, 0, shift)
                f_shifts = torch.flip(f_shifts, dims=(0,))

                if transpose == "reflect":
                    t_shifts = get_space(width, 0, shift)
                    t_shifts = torch.flip(t_shifts, dims=(0,))
            elif shift_type == 3:
                f_shifts = get_space(height, 0, shift)

                if transpose == "reflect":
                    t_shifts = get_space(width, 0, shift)
            elif shift_type == 4:
                f_shifts = get_space(height, shift, shift)

                if transpose == "reflect":
                    t_shifts = get_space(width, shift, shift)
            else:
                raise ValueError("Not existing shift_type.")

            if mixing_type == 1:
                f_shifts = f_shifts
                s_shifts = -f_shifts

                if transpose == "reflect":
                    t_shifts = t_shifts
                    c_shifts = -t_shifts
            elif mixing_type == 2:
                f_shifts = -f_shifts
                s_shifts = f_shifts

                if transpose == "reflect":
                    t_shifts = -t_shifts
                    c_shifts = t_shifts
            elif mixing_type == 3:
                f_shifts = f_shifts
                s_shifts = f_shifts

                if transpose == "reflect":
                    t_shifts = t_shifts
                    c_shifts = t_shifts
            elif mixing_type == 4:
                f_shifts = -f_shifts
                s_shifts = -f_shifts

                if transpose == "reflect":
                    t_shifts = -t_shifts
                    c_shifts = -t_shifts
            else:
                raise ValueError("Not existing mixing_type.")

            if colors == "rb":
                def cat(f_value, s_value):
                    return torch.cat([f_value, g, s_value], 2)

                f = r
                s = b
            elif colors == "rg":
                def cat(f_value, s_value):
                    return torch.cat([f_value, s_value, b], 2)

                f = r
                s = g
            elif colors == "gb":
                def cat(f_value, s_value):
                    return torch.cat([r, f_value, s_value], 2)

                f = g
                s = b
            else:
                raise ValueError("Not existing colors.")

            f_pad = F.pad(f.squeeze(), [shift, shift], padding_mode=method).unsqueeze(2)
            s_pad = F.pad(s.squeeze(), [shift, shift], padding_mode=method).unsqueeze(2)

            f_shifted = torch.zeros_like(f_pad)
            s_shifted = torch.zeros_like(s_pad)

            for i in range(height + (shift * 2)):
                f_shifted[i] = torch.roll(f_pad[i], shifts=int(f_shifts[i]), dims=0)
                s_shifted[i] = torch.roll(s_pad[i], shifts=int(s_shifts[i]), dims=0)

            if transpose == "reflect":
                for i in range(width + (shift * 2)):
                    f_shifted[:, i] = torch.roll(f_shifted[:, i], shifts=int(t_shifts[i]), dims=0)
                    s_shifted[:, i] = torch.roll(s_shifted[:, i], shifts=int(c_shifts[i]), dims=0)

            f_result = f_shifted[shift:-shift, shift:-shift, :]
            s_result = s_shifted[shift:-shift, shift:-shift, :]

            img[:, :, 0:3] = cat(f_result, s_result)

            if transpose == "rotate":
                img = img.permute(1, 0, 2)
            elif transpose == "none" or transpose == "reflect":
                pass
            else:
                raise ValueError("Not existing reverse.")

            return img

        return (torch.stack([
            apply(images[i]) for i in range(len(images))
        ]),)


class ImageEffectsLensBokeh:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "blades_shape": ("INT", {
                    "default": 5,
                    "min": 3,
                }),
                "blades_radius": ("INT", {
                    "default": 10,
                    "min": 1,
                }),
                "blades_rotation": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 360.0,
                }),
                "blur_size": ("INT", {
                    "default": 10,
                    "min": 1,
                    "step": 2
                }),
                "blur_type": (["bilateral", "stack", "none"],),
                "method": (["dilate", "filter"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/effects/lens"

    # noinspection PyUnresolvedReferences
    def lens_blur(self, image, blades_shape, blades_radius, blades_rotation, method):
        angles = np.linspace(0, 2 * np.pi, blades_shape + 1)[:-1] + blades_rotation * np.pi / 180
        x = blades_radius * np.cos(angles) + blades_radius
        y = blades_radius * np.sin(angles) + blades_radius
        pts = np.stack([x, y], axis=1).astype(np.int32)

        mask = np.zeros((blades_radius * 2 + 1, blades_radius * 2 + 1), np.uint8)
        cv2.fillPoly(mask, [pts], 255)

        gaussian_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

        if method == "dilate":
            kernel = cv2.filter2D(mask, -1, gaussian_kernel)
            result = cv2.dilate(image, kernel)
        elif method == "filter":
            height, width = image.shape[:2]
            dilate_size = min(height, width) // 512

            if dilate_size > 0:
                image = cv2.dilate(image, np.ones((dilate_size, dilate_size), np.uint8))

            kernel = mask.astype(np.float32) / np.sum(mask)
            kernel = cv2.filter2D(kernel, -1, gaussian_kernel)
            result = cv2.filter2D(image, -1, kernel)
        else:
            raise ValueError("Unsupported method.")

        return result

    def node(self, images, blades_shape, blades_radius, blades_rotation, blur_size, blur_type, method):
        tensor = images.clone().detach()
        blur_size -= 1

        if blur_type == "bilateral":
            tensor = cv2_layer(tensor, lambda x: cv2.bilateralFilter(x, blur_size, -100, 100))
        elif blur_type == "stack":
            tensor = cv2_layer(tensor, lambda x: cv2.stackBlur(x, (blur_size, blur_size)))
        elif blur_type == "none":
            pass
        else:
            raise ValueError("Unsupported blur type.")

        return (cv2_layer(tensor, lambda x: self.lens_blur(
            x, blades_shape, blades_radius, blades_rotation, method
        )),)


class ImageEffectsLensOpticAxis:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "lens_shape": (["circle", "square", "rectangle", "corners"],),
                "lens_edge": (["around", "symmetric"],),
                "lens_curvy": ("FLOAT", {
                    "default": 4.0,
                    "max": 15.0,
                    "step": 0.1,
                }),
                "lens_zoom": ("FLOAT", {
                    "default": 2.0,
                    "step": 0.1,
                }),
                "lens_aperture": ("FLOAT", {
                    "default": 0.5,
                    "max": 10.0,
                    "step": 0.1,
                }),
                "blur_intensity": ("INT", {
                    "default": 30,
                    "min": 2,
                    "step": 2
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "node"
    CATEGORY = "image/effects/lens"

    def node(self, images, lens_shape, lens_edge, lens_curvy, lens_zoom, lens_aperture, blur_intensity):
        blur_intensity -= 1
        lens_zoom += 1

        height, width = images[0, :, :, 0].shape

        if lens_edge == "around":
            mask = radialspace_2D((height, width), lens_curvy, lens_zoom, lens_shape, 0.0, 1.0 + lens_curvy).unsqueeze(0).unsqueeze(3)
        elif lens_edge == "symmetric":
            if height != width:
                new_height = new_width = max(height, width)
                crop_top_bottom = (new_height - height) // 2
                crop_left_right = (new_width - width) // 2

                mask = radialspace_2D((new_height, new_width), lens_curvy, lens_zoom, lens_shape, 0.0, 1.0 + lens_curvy)[
                   crop_top_bottom:-crop_top_bottom or None,
                   crop_left_right:-crop_left_right or None
                ].unsqueeze(0).unsqueeze(3)
            else:
                mask = radialspace_2D((height, width), lens_curvy, lens_zoom, lens_shape, 0.0, 1.0 + lens_curvy).unsqueeze(0).unsqueeze(3)
        else:
            raise ValueError("Not existing lens_edge parameter.")

        center_x = width // 2
        center_y = height // 2

        y_v, x_v = torch.meshgrid(torch.arange(height), torch.arange(width), indexing='ij')

        dx = x_v - center_x
        dy = y_v - center_y

        distance = torch.sqrt(dx ** 2 + dy ** 2)

        map_x = x_v + mask[0, :, :, 0] * dx / distance * (-lens_aperture * 100)
        map_y = y_v + mask[0, :, :, 0] * dy / distance * (-lens_aperture * 100)

        map_x = map_x.to(torch.float32).numpy()
        map_y = map_y.to(torch.float32).numpy()

        shifted_images = cv2_layer(images, lambda x: cv2.remap(x, map_x, map_y, cv2.INTER_LINEAR))
        shifted_mask = cv2_layer(mask, lambda x: cv2.remap(x, map_x, map_y, cv2.INTER_LINEAR))
        edited_images = cv2_layer(shifted_images, lambda x: cv2.stackBlur(x, (blur_intensity, blur_intensity)))

        mask = torch.clamp(mask, 0.0, 1.0)
        shifted_mask = torch.clamp(shifted_mask, 0.0, 1.0)

        result = shifted_images * (1 - mask) + edited_images * mask

        return result, shifted_mask


class ImageEffectsLensVignette:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "lens_shape": (["circle", "rectangle"],),
                "lens_edge": (["around", "symmetric"],),
                "lens_curvy": ("FLOAT", {
                    "default": 3.0,
                    "max": 15.0,
                    "step": 0.1,
                }),
                "lens_zoom": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.1,
                }),
                "brightness": ("FLOAT", {
                    "default": 0.25,
                    "max": 1.0,
                    "step": 0.01
                }),
                "saturation": ("FLOAT", {
                    "default": 0.5,
                    "max": 1.0,
                    "step": 0.01
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "node"
    CATEGORY = "image/effects/lens"

    def node(self, images, lens_shape, lens_edge, lens_curvy, lens_zoom, brightness, saturation):
        tensor = images.clone().detach()

        lens_zoom += 1

        height, width = tensor[0, :, :, 0].shape

        if lens_edge == "around":
            mask = radialspace_2D((height, width), lens_curvy, lens_zoom, lens_shape).unsqueeze(0).unsqueeze(3)
        elif lens_edge == "symmetric":
            if height != width:
                new_height = new_width = max(height, width)
                crop_top_bottom = (new_height - height) // 2
                crop_left_right = (new_width - width) // 2

                mask = radialspace_2D((new_height, new_width), lens_curvy, lens_zoom, lens_shape)[
                       crop_top_bottom:-crop_top_bottom or None,
                       crop_left_right:-crop_left_right or None
                ].unsqueeze(0).unsqueeze(3)
            else:
                mask = radialspace_2D((height, width), lens_curvy, lens_zoom, lens_shape).unsqueeze(0).unsqueeze(3)
        else:
            raise ValueError("Not existing lens_edge parameter.")

        tensor = tensor.permute(0, 3, 1, 2)
        tensor[:, 0:3, :, :] = F.adjust_brightness(tensor[:, 0:3, :, :], brightness)
        tensor[:, 0:3, :, :] = F.adjust_saturation(tensor[:, 0:3, :, :], saturation)
        tensor = tensor.permute(0, 2, 3, 1)

        result = images * (1 - mask) + tensor * mask

        mask = mask.squeeze()

        return result, mask


NODE_CLASS_MAPPINGS = {
    "ImageEffectsAdjustment": ImageEffectsAdjustment,
    "ImageEffectsGrayscale": ImageEffectsGrayscale,
    "ImageEffectsNegative": ImageEffectsNegative,
    "ImageEffectsSepia": ImageEffectsSepia,
    "ImageEffectsLensZoomBurst": ImageEffectsLensZoomBurst,
    "ImageEffectsLensChromaticAberration": ImageEffectsLensChromaticAberration,
    "ImageEffectsLensBokeh": ImageEffectsLensBokeh,
    "ImageEffectsLensOpticAxis": ImageEffectsLensOpticAxis,
    "ImageEffectsLensVignette": ImageEffectsLensVignette
}
