from typing import Literal

import numpy as np
import torch
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


def cv2_layer(tensor: Tensor, function) -> Tensor:
    """
    This function applies a given function to each channel of an input tensor and returns the result as a PyTorch tensor.

    :param tensor: A PyTorch tensor of shape (H, W, C) or (N, H, W, C), where C is the number of channels, H is the height, and W is the width of the image.
    :param function: A function that takes a numpy array of shape (H, W, C) as input and returns a numpy array of the same shape.
    :return: A PyTorch tensor of the same shape as the input tensor, where the given function has been applied to each channel of each image in the tensor.
    """
    shape_size = tensor.shape.__len__()

    def produce(image):
        channels = image[0, 0, :].shape[0]

        rgb = image[:, :, 0:3].numpy()
        result_rgb = function(rgb)

        if channels == 3:
            return torch.from_numpy(result_rgb)
        elif channels == 4:
            alpha = image[:, :, 3:4].numpy()
            result_alpha = function(alpha)[..., np.newaxis]
            result_rgba = np.concatenate((result_rgb, result_alpha), axis=2)

            return torch.from_numpy(result_rgba)

    if shape_size == 3:
        return torch.from_numpy(produce(tensor))
    elif shape_size == 4:
        return torch.stack([
            produce(tensor[i]) for i in range(len(tensor))
        ])
    else:
        raise ValueError("Incompatible tensor dimension.")


Tensor.tensor_to_image = tensor_to_image
ImageB.image_to_tensor = image_to_tensor
