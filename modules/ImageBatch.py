import re

import torch


class ImageBatchGet:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "index": ("INT", {
                    "default": 1,
                    "min": 1,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/batch"

    def node(self, images, index):
        batch = images.shape[0]
        index = min(batch, index - 1)

        return (images[index].unsqueeze(0),)


class ImageBatchRemove:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "index": ("INT", {
                    "default": 1,
                    "min": 1,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/batch"

    def node(self, images, index):
        batch = images.shape[0]
        index = min(batch, index - 1)

        return (torch.cat((images[:index], images[index + 1:]), dim=0),)


class ImageBatchFork:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "priority": (["first", "second"],),
            },
        }

    RETURN_TYPES = ("IMAGE", "IMAGE")
    FUNCTION = "node"
    CATEGORY = "image/batch"

    def node(self, images, priority):
        batch = images.shape[0]

        if batch == 1:
            return images, images
        elif batch % 2 == 0:
            first = batch // 2
            second = batch // 2
        else:
            if priority == "first":
                first = batch // 2 + 1
                second = batch // 2
            elif priority == "second":
                first = batch // 2
                second = batch // 2 + 1
            else:
                raise ValueError("Not existing priority.")

        return images[:first], images[-second:]


class ImageBatchJoin:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images_a": ("IMAGE",),
                "images_b": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/batch"

    def node(self, images_a, images_b):
        height_a, width_a, channels_a = images_a[0].shape
        height_b, width_b, channels_b = images_b[0].shape

        if height_a != height_b:
            raise ValueError("Height of images_a not equals of images_b. You can use ImageTransformResize for fix it.")

        if width_a != width_b:
            raise ValueError("Width of images_a not equals of images_b. You can use ImageTransformResize for fix it.")

        if channels_a != channels_b:
            raise ValueError("Channels of images_a not equals of images_b. Your can add or delete alpha channels with AlphaChanel module.")

        return (torch.cat((images_a, images_b)),)


class ImageBatchPermute:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "permute": ("STRING", {"multiline": False}),
                "start_with_zero": ("BOOLEAN",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/batch"

    def node(self, images, permute, start_with_zero):
        order = [int(num) - 1 if not start_with_zero else int(num) for num in re.findall(r'\d+', permute)]
        order = torch.tensor(order)
        order = order.clamp(0, images.shape[0] - 1)

        return (images.index_select(0, order),)


NODE_CLASS_MAPPINGS = {
    "ImageBatchGet": ImageBatchGet,
    "ImageBatchRemove": ImageBatchRemove,
    "ImageBatchFork": ImageBatchFork,
    "ImageBatchJoin": ImageBatchJoin,
    "ImageBatchPermute": ImageBatchPermute
}
