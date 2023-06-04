import torch

from .Utils import create_rgba_image


class ImageContainer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {
                    "default": 512,
                    "step": 1
                }),
                "height": ("INT", {
                    "default": 512,
                    "step": 1
                }),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_container"
    CATEGORY = "image"

    def image_container(self, width, height, red, green, blue, alpha):
        return (create_rgba_image(width, height, (red, green, blue, int(alpha * 255))).image_to_tensor().unsqueeze(0),)


class ImageContainerInheritanceAdd:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "add_width": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "add_height": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "method": (["single", "for_each"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_container_inheritance_add"
    CATEGORY = "image"

    def image_container_inheritance_add(self, images, add_width, add_height, red, green, blue, alpha, method):
        width, height = images[0, :, :, 0].shape

        width = width + add_width
        height = height + add_height

        image = create_rgba_image(width, height, (red, green, blue, int(alpha * 255))).image_to_tensor()

        if method == "single":
            return (image.unsqueeze(0),)
        else:
            length = len(images)

            images = torch.zeros(length, height, width, 4)
            images[:, :, :] = image
            return (images,)


class ImageContainerInheritanceScale:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "scale_width": ("FLOAT", {
                    "default": 1.0,
                    "step": 0.1
                }),
                "scale_height": ("FLOAT", {
                    "default": 1.0,
                    "step": 0.1
                }),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "method": (["single", "for_each"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_container_inheritance_scale"
    CATEGORY = "image"

    def image_container_inheritance_scale(self, images, scale_width, scale_height, red, green, blue, alpha, method):
        width, height = images[0, :, :, 0].shape

        width = int((width * scale_width) - width)
        height = int((height * scale_height) - height)

        return ImageContainerInheritanceAdd() \
            .image_container_inheritance_add(images, width, height, red, green, blue, alpha, method)


class ImageContainerInheritanceMax:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images_a": ("IMAGE",),
                "images_b": ("IMAGE",),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "method": (["single", "for_each_pair", "for_each_matrix"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_container_inheritance_max"
    CATEGORY = "image"

    def image_container_inheritance_max(self, images_a, images_b, red, green, blue, alpha, method):
        img_a_height, img_a_width = images_a[0, :, :, 0].shape
        img_b_height, img_b_width = images_b[0, :, :, 0].shape

        width = max(img_a_width, img_b_width)
        height = max(img_a_height, img_b_height)

        image = create_rgba_image(width, height, (red, green, blue, int(alpha * 255))).image_to_tensor()

        if method == "single":
            return (image.unsqueeze(0),)
        elif method == "for_each_pair":
            length = len(images_a)
            images = torch.zeros(length, height, width, 4)
        else:
            length = len(images_a) * len(images_b)
            images = torch.zeros(length, height, width, 4)

        images[:, :, :] = image
        return (images,)


class ImageContainerInheritanceSum:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images_a": ("IMAGE",),
                "images_b": ("IMAGE",),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "container_size_type": (["sum", "sum_width", "sum_height"],),
                "method": (["single", "for_each_pair", "for_each_matrix"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_container_inheritance_sum"
    CATEGORY = "image"

    def image_container_inheritance_sum(self, images_a, images_b, red, green, blue, alpha, container_size_type, method):
        img_a_height, img_a_width = images_a[0, :, :, 0].shape
        img_b_height, img_b_width = images_b[0, :, :, 0].shape

        if container_size_type == "sum":
            width = img_a_width + img_b_width
            height = img_a_height + img_b_height
        elif container_size_type == "sum_width":
            if img_a_height != img_b_height:
                raise ValueError()

            width = img_a_width + img_b_width
            height = img_a_height
        elif container_size_type == "sum_height":
            if img_a_width != img_b_width:
                raise ValueError()

            width = img_a_width
            height = img_a_height + img_b_height
        else:
            raise ValueError()

        image = create_rgba_image(width, height, (red, green, blue, int(alpha * 255))).image_to_tensor()

        if method == "single":
            return (image.unsqueeze(0),)
        elif method == "for_each_pair":
            length = len(images_a)
            images = torch.zeros(length, height, width, 4)
        else:
            length = len(images_a) * len(images_b)
            images = torch.zeros(length, height, width, 4)

        images[:, :, :] = image
        return (images,)


NODE_CLASS_MAPPINGS = {
    "ImageContainer": ImageContainer,
    "ImageContainerInheritanceAdd": ImageContainerInheritanceAdd,
    "ImageContainerInheritanceScale": ImageContainerInheritanceScale,
    "ImageContainerInheritanceMax": ImageContainerInheritanceMax,
    "ImageContainerInheritanceSum": ImageContainerInheritanceSum
}
