import cv2
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
    "ImageEffectsLensChromaticAberration": ImageEffectsLensChromaticAberration,
    "ImageEffectsLensOpticAxis": ImageEffectsLensOpticAxis,
    "ImageEffectsLensVignette": ImageEffectsLensVignette
}
