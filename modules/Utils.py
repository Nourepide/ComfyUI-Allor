from typing import Literal

import torchvision.transforms as t
from PIL import Image as ImageF
from PIL.Image import Image as ImageB
from torch import Tensor


def tensor_to_image(self):
    return t.ToPILImage()(self.permute(2, 0, 1))


def image_to_tensor(self):
    return t.ToTensor()(self).permute(1, 2, 0)


def create_rgba_image(width: int, height: int, color=(0, 0, 0, 0)) -> ImageB:
    return ImageF.new("RGBA", (width, height), color)


def get_sampler_by_name(method) -> Literal[0, 1, 2, 3, 4, 5]:
    if method == "lanczos":
        return ImageF.LANCZOS
    elif method == "bicubic":
        return ImageF.BICUBIC
    elif method == "hamming":
        return ImageF.HAMMING
    elif method == "bilinear":
        return ImageF.BILINEAR
    elif method == "box":
        return ImageF.BOX
    elif method == "nearest":
        return ImageF.NEAREST
    else:
        raise ValueError("Sampler not found.")


Tensor.tensor_to_image = tensor_to_image
ImageB.image_to_tensor = image_to_tensor
