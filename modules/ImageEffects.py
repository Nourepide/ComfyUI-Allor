import torch

import torchvision.transforms.functional as F


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
    FUNCTION = "image_effects_adjustment"
    CATEGORY = "image/effects"

    def image_effects_adjustment(self, images, brightness, contrast, saturation, hue, gamma, sharpness, red, green, blue):
        # noinspection PyUnboundLocalVariable
        def apply(img):
            rgba = False

            if len(img[0, 0, :]) == 4:
                a = img[:, :, 3].unsqueeze(2)
                img = img[:, :, 0:3]
                rgba = True

            img = img.permute(2, 0, 1)
            img = F.adjust_brightness(img, brightness)
            img = F.adjust_contrast(img, contrast)
            img = F.adjust_saturation(img, saturation)
            img = F.adjust_hue(img, hue - 0.5)
            img = F.adjust_gamma(img, gamma)
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
    FUNCTION = "image_effects_grayscale"
    CATEGORY = "image/effects"

    def image_effects_grayscale(self, images):
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
    FUNCTION = "image_effects_negative"
    CATEGORY = "image/effects"

    def image_effects_negative(self, images):
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
    FUNCTION = "image_effects_sepia"
    CATEGORY = "image/effects"

    def image_effects_sepia(self, images):
        tensor = images.clone().detach()

        sepia_mask = torch.tensor([[0.393, 0.349, 0.272],
                                   [0.769, 0.686, 0.534],
                                   [0.189, 0.168, 0.131]])

        tensor[:, :, :, 0:3] = torch.stack([
            torch.matmul(tensor[i, :, :, 0:3], sepia_mask) for i in range(len(tensor))
        ])

        return (tensor,)


class ImageEffectsChromaticAberration:
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
                "curvy": ("FLOAT", {
                    "default": 1.0,
                    "max": 15.0,
                    "step": 0.1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_effects_chromatic_aberration"
    CATEGORY = "image/effects"

    def image_effects_chromatic_aberration(self, images, shift, method, shift_type, mixing_type, transpose, colors, curvy):
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

            def get_space(start, end, steps, strength):
                steps += shift * 2

                if start == end:
                    return torch.full((steps,), start)

                tensor = torch.linspace(start, end, steps)
                tensor = torch.sign(tensor) * (torch.abs(tensor) ** strength)
                tensor = ((tensor - tensor.min()) / (tensor.max() - tensor.min())) * (end - start) + start

                return tensor

            if shift_type == 1:
                f_shifts = get_space(-shift, shift, height, curvy)

                if transpose == "reflect":
                    t_shifts = get_space(-shift, shift, width, curvy)
            elif shift_type == 2:
                f_shifts = get_space(0, shift, height, curvy)
                f_shifts = torch.flip(f_shifts, dims=(0,))

                if transpose == "reflect":
                    t_shifts = get_space(0, shift, width, curvy)
                    t_shifts = torch.flip(t_shifts, dims=(0,))
            elif shift_type == 3:
                f_shifts = get_space(0, shift, height, curvy)

                if transpose == "reflect":
                    t_shifts = get_space(0, shift, width, curvy)
            elif shift_type == 4:
                f_shifts = get_space(shift, shift, height, curvy)

                if transpose == "reflect":
                    t_shifts = get_space(shift, shift, width, curvy)
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


NODE_CLASS_MAPPINGS = {
    "ImageEffectsAdjustment": ImageEffectsAdjustment,
    "ImageEffectsGrayscale": ImageEffectsGrayscale,
    "ImageEffectsNegative": ImageEffectsNegative,
    "ImageEffectsSepia": ImageEffectsSepia,
    "ImageEffectsChromaticAberration": ImageEffectsChromaticAberration,
}
