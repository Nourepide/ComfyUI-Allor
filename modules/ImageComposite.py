import torch
from PIL import Image as ImageF


class ImageCompositeAbsolute:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images_a": ("IMAGE",),
                "images_b": ("IMAGE",),
                "images_a_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "images_a_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "images_b_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "images_b_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "container_width": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "container_height": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "background": (["images_a", "images_b"],),
                "method": (["pair", "matrix"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/composite"

    def node(
            self,
            images_a,
            images_b,
            images_a_x,
            images_a_y,
            images_b_x,
            images_b_y,
            container_width,
            container_height,
            background,
            method
    ):
        def clip(value: float):
            return value if value >= 0 else 0

        # noinspection PyUnresolvedReferences
        def composite(image_a, image_b):
            img_a_height, img_a_width, img_a_dim = image_a.shape
            img_b_height, img_b_width, img_b_dim = image_b.shape

            if img_a_dim == 3:
                image_a = torch.stack([
                    image_a[:, :, 0],
                    image_a[:, :, 1],
                    image_a[:, :, 2],
                    torch.ones((img_a_height, img_a_width))
                ], dim=2)

            if img_b_dim == 3:
                image_b = torch.stack([
                    image_b[:, :, 0],
                    image_b[:, :, 1],
                    image_b[:, :, 2],
                    torch.ones((img_b_height, img_b_width))
                ], dim=2)

            container_x = max(img_a_width, img_b_width) if container_width == 0 else container_width
            container_y = max(img_a_height, img_b_height) if container_height == 0 else container_height

            container_a = torch.zeros((container_y, container_x, 4))
            container_b = torch.zeros((container_y, container_x, 4))

            img_a_height_c, img_a_width_c = [
                clip((images_a_y + img_a_height) - container_y),
                clip((images_a_x + img_a_width) - container_x)
            ]

            img_b_height_c, img_b_width_c = [
                clip((images_b_y + img_b_height) - container_y),
                clip((images_b_x + img_b_width) - container_x)
            ]

            if img_a_height_c <= img_a_height and img_a_width_c <= img_a_width:
                container_a[
                    images_a_y:img_a_height + images_a_y - img_a_height_c,
                    images_a_x:img_a_width + images_a_x - img_a_width_c
                ] = image_a[
                    :img_a_height - img_a_height_c,
                    :img_a_width - img_a_width_c
                ]

            if img_b_height_c <= img_b_height and img_b_width_c <= img_b_width:
                container_b[
                    images_b_y:img_b_height + images_b_y - img_b_height_c,
                    images_b_x:img_b_width + images_b_x - img_b_width_c
                ] = image_b[
                    :img_b_height - img_b_height_c,
                    :img_b_width - img_b_width_c
                ]

            if background == "images_a":
                return ImageF.alpha_composite(
                    container_a.tensor_to_image(),
                    container_b.tensor_to_image()
                ).image_to_tensor()
            else:
                return ImageF.alpha_composite(
                    container_b.tensor_to_image(),
                    container_a.tensor_to_image()
                ).image_to_tensor()

        if method == "pair":
            if len(images_a) != len(images_b):
                raise ValueError("Size of image_a and image_b not equals for pair batch type.")

            return (torch.stack([
                composite(images_a[i], images_b[i]) for i in range(len(images_a))
            ]),)
        elif method == "matrix":
            return (torch.stack([
                composite(images_a[i], images_b[j]) for i in range(len(images_a)) for j in range(len(images_b))
            ]),)

        return None


class ImageCompositeAbsoluteByContainer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "container": ("IMAGE",),
                "images_a": ("IMAGE",),
                "images_b": ("IMAGE",),
                "images_a_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "images_a_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "images_b_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "images_b_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "background": (["images_a", "images_b"],),
                "method": (["pair", "matrix"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/composite"

    def node(
            self,
            container,
            images_a,
            images_b,
            images_a_x,
            images_a_y,
            images_b_x,
            images_b_y,
            background,
            method
    ):
        return ImageCompositeAbsolute().node(
            images_a,
            images_b,
            images_a_x,
            images_a_y,
            images_b_x,
            images_b_y,
            container[0, :, :, 0].shape[1],
            container[0, :, :, 0].shape[0],
            background,
            method
        )


class ImageCompositeRelative:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images_a": ("IMAGE",),
                "images_b": ("IMAGE",),
                "images_a_x": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "images_a_y": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "images_b_x": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "images_b_y": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "background": (["images_a", "images_b"],),
                "container_size_type": (["max", "sum", "sum_width", "sum_height"],),
                "method": (["pair", "matrix"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/composite"

    def node(
            self,
            images_a,
            images_b,
            images_a_x,
            images_a_y,
            images_b_x,
            images_b_y,
            background,
            container_size_type,
            method
    ):
        def offset_by_percent(container_size: int, image_size: int, percent: float):
            return int((container_size - image_size) * percent)

        img_a_height, img_a_width = images_a[0, :, :, 0].shape
        img_b_height, img_b_width = images_b[0, :, :, 0].shape

        if container_size_type == "max":
            container_width = max(img_a_width, img_b_width)
            container_height = max(img_a_height, img_b_height)
        elif container_size_type == "sum":
            container_width = img_a_width + img_b_width
            container_height = img_a_height + img_b_height
        elif container_size_type == "sum_width":
            if img_a_height != img_b_height:
                raise ValueError()

            container_width = img_a_width + img_b_width
            container_height = img_a_height
        elif container_size_type == "sum_height":
            if img_b_width != img_b_width:
                raise ValueError()

            container_width = img_a_width
            container_height = img_a_height + img_a_height
        else:
            raise ValueError()

        return ImageCompositeAbsolute().node(
            images_a,
            images_b,
            offset_by_percent(container_width, img_a_width, images_a_x),
            offset_by_percent(container_height, img_a_height, images_a_y),
            offset_by_percent(container_width, img_b_width, images_b_x),
            offset_by_percent(container_height, img_b_height, images_b_y),
            container_width,
            container_height,
            background,
            method
        )


class ImageCompositeRelativeByContainer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "container": ("IMAGE",),
                "images_a": ("IMAGE",),
                "images_b": ("IMAGE",),
                "images_a_x": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "images_a_y": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "images_b_x": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "images_b_y": ("FLOAT", {
                    "default": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "background": (["images_a", "images_b"],),
                "method": (["pair", "matrix"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/composite"

    def node(
            self,
            container,
            images_a,
            images_b,
            images_a_x,
            images_a_y,
            images_b_x,
            images_b_y,
            background,
            method
    ):
        def offset_by_percent(container_size: int, image_size: int, percent: float):
            return int((container_size - image_size) * percent)

        img_a_height, img_a_width = images_a[0, :, :, 0].shape
        img_b_height, img_b_width = images_b[0, :, :, 0].shape

        container_width = container[0, :, :, 0].shape[1]
        container_height = container[0, :, :, 0].shape[0]

        if container_width < max(img_a_width, img_b_width) or container_height < max(img_a_height, img_b_height):
            raise ValueError("Container can't be smaller then max width or height of images.")

        return ImageCompositeAbsolute().node(
            images_a,
            images_b,
            offset_by_percent(container_width, img_a_width, images_a_x),
            offset_by_percent(container_height, img_a_height, images_a_y),
            offset_by_percent(container_width, img_b_width, images_b_x),
            offset_by_percent(container_height, img_b_height, images_b_y),
            container_width,
            container_height,
            background,
            method
        )


NODE_CLASS_MAPPINGS = {
    "ImageCompositeAbsolute": ImageCompositeAbsolute,
    "ImageCompositeAbsoluteByContainer": ImageCompositeAbsoluteByContainer,
    "ImageCompositeRelative": ImageCompositeRelative,
    "ImageCompositeRelativeByContainer": ImageCompositeRelativeByContainer
}
