import torch
import torchvision.transforms.functional as TF
from PIL import Image, ImageDraw

from .Utils import get_sampler_by_name


class ImageTransformResizeAbsolute:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "width": ("INT", {
                    "default": 256,
                    "min": 1,
                    "step": 1
                }),
                "height": ("INT", {
                    "default": 256,
                    "min": 1,
                    "step": 1
                }),
                "method": (["lanczos", "bicubic", "hamming", "bilinear", "box", "nearest"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/transform"

    def node(self, images, width, height, method):
        def resize_tensor(tensor):
            return tensor.tensor_to_image().resize((width, height), get_sampler_by_name(method)).image_to_tensor()

        return (torch.stack([
            resize_tensor(images[i]) for i in range(len(images))
        ]),)


class ImageTransformResizeRelative:
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
                "method": (["lanczos", "bicubic", "hamming", "bilinear", "box", "nearest"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/transform"

    def node(self, images, scale_width, scale_height, method):
        height, width = images[0, :, :, 0].shape

        width = int(width * scale_width)
        height = int(height * scale_height)

        return ImageTransformResizeAbsolute().node(images, width, height, method)


class ImageTransformResizeClip:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "max_width": ("INT", {
                    "default": 1024,
                }),
                "max_height": ("INT", {
                    "default": 1024,
                }),
                "min_width": ("INT", {
                    "default": 0,
                }),
                "min_height": ("INT", {
                    "default": 0,
                }),
                "method": (["lanczos", "bicubic", "hamming", "bilinear", "box", "nearest"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/transform"

    def node(self, images, max_width, max_height, min_width, min_height, method):
        height, width = images[0, :, :, 0].shape

        if min_width >= max_width and min_height >= max_height:
            return (images,)

        scale_min = max(min_width / width, min_height / height)
        scale_max = min(max_width / width, max_height / height)

        scale = max(scale_min, scale_max)

        width = int(width * scale)
        height = int(height * scale)

        return ImageTransformResizeAbsolute().node(images, width, height, method)


class ImageTransformCropAbsolute:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "start_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "start_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "end_x": ("INT", {
                    "default": 128,
                    "step": 1
                }),
                "end_y": ("INT", {
                    "default": 128,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/transform"

    def node(self, images, start_x, start_y, end_x, end_y):
        def resize_tensor(tensor):
            return tensor.tensor_to_image().crop([start_x, start_y, end_x, end_y]).image_to_tensor()

        return (torch.stack([
            resize_tensor(images[i]) for i in range(len(images))
        ]),)


class ImageTransformCropRelative:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "start_x": ("FLOAT", {
                    "default": 0.25,
                    "max": 1.0,
                    "step": 0.01
                }),
                "start_y": ("FLOAT", {
                    "default": 0.25,
                    "max": 1.0,
                    "step": 0.01
                }),
                "end_x": ("FLOAT", {
                    "default": 0.75,
                    "max": 1.0,
                    "step": 0.01
                }),
                "end_y": ("FLOAT", {
                    "default": 0.75,
                    "max": 1.0,
                    "step": 0.01
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/transform"

    def node(self, images, start_x, start_y, end_x, end_y):
        height, width = images[0, :, :, 0].shape

        return ImageTransformCropAbsolute().node(
            images,
            width * start_x,
            height * start_y,
            width * end_x,
            height * end_y
        )


class ImageTransformCropCorners:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "radius": ("INT", {
                    "default": 180,
                    "max": 360,
                    "step": 1
                }),
                "top_left_corner": (["true", "false"],),
                "top_right_corner": (["true", "false"],),
                "bottom_right_corner": (["true", "false"],),
                "bottom_left_corner": (["true", "false"],),
                "SSAA": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 16,
                    "step": 1
                }),
                "method": (["lanczos", "bicubic", "hamming", "bilinear", "box", "nearest"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/transform"

    # noinspection PyUnresolvedReferences, PyArgumentList
    def node(
            self,
            images,
            radius,
            top_left_corner,
            top_right_corner,
            bottom_right_corner,
            bottom_left_corner,
            SSAA,
            method
    ):
        sampler = get_sampler_by_name(method)

        height, width = images[0, :, :, 0].shape

        canvas = Image.new("RGBA", (width * SSAA, height * SSAA), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        draw.rounded_rectangle(
            ((0, 0), (width * SSAA, height * SSAA)),
            radius * SSAA, (255, 255, 255, 255),
            corners=(
                True if top_left_corner == "true" else False,
                True if top_right_corner == "true" else False,
                True if bottom_right_corner == "true" else False,
                True if bottom_left_corner == "true" else False
            )
        )

        canvas = canvas.resize((width, height), sampler)
        mask = 1.0 - canvas.image_to_tensor()[:, :, 3]

        def crop_tensor(tensor):
            return torch.stack([
                (tensor[:, :, i] - mask).clamp(0, 1) for i in range(tensor.shape[2])
            ], dim=2)

        return (torch.stack([
            crop_tensor(images[i]) for i in range(len(images))
        ]),)


class ImageTransformPaddingAbsolute:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "add_width": ("INT", {
                    "default": 64,
                    "min": 0,
                }),
                "add_height": ("INT", {
                    "default": 64,
                    "min": 0,
                }),
                "method": (["reflect", "edge", "constant"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/transform"

    def node(self, images, add_width, add_height, method):
        def transpose_tensor(image):
            tensor = image.clone().detach()
            tensor_pad = TF.pad(tensor.permute(2, 0, 1), [add_height, add_width], padding_mode=method).permute(1, 2, 0)

            return tensor_pad

        return (torch.stack([
            transpose_tensor(images[i]) for i in range(len(images))
        ]),)


class ImageTransformPaddingRelative:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "scale_width": ("FLOAT", {
                    "default": 0.25,
                    "step": 0.1,
                }),
                "scale_height": ("FLOAT", {
                    "default": 0.25,
                    "step": 0.1,
                }),
                "method": (["reflect", "edge", "constant"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/transform"

    def node(self, images, scale_width, scale_height, method):
        height, width = images[0, :, :, 0].shape

        add_width = int(width * scale_width)
        add_height = int(height * scale_height)

        return ImageTransformPaddingAbsolute().node(images, add_width, add_height, method)


class ImageTransformRotate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "angle": ("FLOAT", {
                    "default": 35.0,
                    "max": 360.0,
                    "step": 0.1
                }),
                "expand": (["true", "false"],),
                "SSAA": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 16,
                    "step": 1
                }),
                "method": (["lanczos", "bicubic", "hamming", "bilinear", "box", "nearest"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/transform"

    def node(self, images, angle, expand, SSAA, method):
        height, width = images[0, :, :, 0].shape

        def rotate_tensor(tensor):
            if method == "lanczos":
                resize_sampler = Image.LANCZOS
                rotate_sampler = Image.BICUBIC
            elif method == "bicubic":
                resize_sampler = Image.BICUBIC
                rotate_sampler = Image.BICUBIC
            elif method == "hamming":
                resize_sampler = Image.HAMMING
                rotate_sampler = Image.BILINEAR
            elif method == "bilinear":
                resize_sampler = Image.BILINEAR
                rotate_sampler = Image.BILINEAR
            elif method == "box":
                resize_sampler = Image.BOX
                rotate_sampler = Image.NEAREST
            elif method == "nearest":
                resize_sampler = Image.NEAREST
                rotate_sampler = Image.NEAREST
            else:
                raise ValueError()

            if SSAA > 1:
                img = tensor.tensor_to_image()
                img_us_scaled = img.resize((width * SSAA, height * SSAA), resize_sampler)
                img_rotated = img_us_scaled.rotate(angle, rotate_sampler, expand == "true", fillcolor=(0, 0, 0, 0))
                img_down_scaled = img_rotated.resize((img_rotated.width // SSAA, img_rotated.height // SSAA), resize_sampler)
                result = img_down_scaled.image_to_tensor()
            else:
                img = tensor.tensor_to_image()
                img_rotated = img.rotate(angle, rotate_sampler, expand == "true", fillcolor=(0, 0, 0, 0))
                result = img_rotated.image_to_tensor()

            return result

        if angle == 0.0 or angle == 360.0:
            return (images,)
        else:
            return (torch.stack([
                rotate_tensor(images[i]) for i in range(len(images))
            ]),)


class ImageTransformTranspose:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "method": (["flip_horizontally", "flip_vertically", "rotate_90", "rotate_180", "rotate_270", "transpose", "transverse"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/transform"

    def node(self, images, method):
        def transpose_tensor(tensor):
            if method == "flip_horizontally":
                transpose = Image.FLIP_LEFT_RIGHT
            elif method == "flip_vertically":
                transpose = Image.FLIP_TOP_BOTTOM
            elif method == "rotate_90":
                transpose = Image.ROTATE_90
            elif method == "rotate_180":
                transpose = Image.ROTATE_180
            elif method == "rotate_270":
                transpose = Image.ROTATE_270
            elif method == "transpose":
                transpose = Image.TRANSPOSE
            elif method == "transverse":
                transpose = Image.TRANSVERSE
            else:
                raise ValueError()

            return tensor.tensor_to_image().transpose(transpose).image_to_tensor()

        return (torch.stack([
            transpose_tensor(images[i]) for i in range(len(images))
        ]),)


NODE_CLASS_MAPPINGS = {
    "ImageTransformResizeAbsolute": ImageTransformResizeAbsolute,
    "ImageTransformResizeRelative": ImageTransformResizeRelative,
    "ImageTransformResizeClip": ImageTransformResizeClip,
    "ImageTransformCropAbsolute": ImageTransformCropAbsolute,
    "ImageTransformCropRelative": ImageTransformCropRelative,
    "ImageTransformCropCorners": ImageTransformCropCorners,
    "ImageTransformPaddingAbsolute": ImageTransformPaddingAbsolute,
    "ImageTransformPaddingRelative": ImageTransformPaddingRelative,
    "ImageTransformRotate": ImageTransformRotate,
    "ImageTransformTranspose": ImageTransformTranspose
}
