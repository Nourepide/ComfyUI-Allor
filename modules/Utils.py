from typing import Literal, Any

import numpy as np
import torch
import torchvision.transforms as t
from PIL import Image as ImageF
from PIL.Image import Image as ImageB
from torch import Tensor, dtype


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

        if channels <= 3:
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


def radialspace_1D(
        size: int,
        curvy: float = 1.0,
        scale: float = 1.0,
        min_val: float = 0.0,
        max_val: float = 1.0,
        normalize: bool = True,
        dtype: dtype = torch.float32
):
    """
    Create a 1D tensor with a radial gradient from 0 to 1 from the center to the edges.

    :param size: Tuple of int
        Size of the tensor.
        Can be a tuple of one or two integers.
        If one integer is given, the tensor will be square.
        If two integers are given, the tensor will have the given width and height.
    :param curvy: Float
        Curviness of the gradient.
        Higher values result in a sharper transition from 0 to 1.
    :param scale: Float
        Scale of the gradient.
        Higher values result in a larger area with values close to 1.
    :param min_val: Float
        Minimum value in the tensor.
    :param max_val: Float
        Maximum value in the tensor.
    :param normalize: Bool
        Whether to normalize the tensor values to be between min_val and max_val.
    :param dtype: Torch.dtype
        Data type of the resulting tensor.

    :return: Torch.Tensor
        A 2D tensor with a radial gradient from 0 to 1 from the center to the edges.
    """

    tensor = radialspace_2D((1, size), curvy, scale, "square", min_val, max_val, (0.0, 0.5), None, normalize, dtype).squeeze()

    if min_val < 0:
        tensor[:len(tensor) // 2] = -(tensor[:len(tensor) // 2])

    if normalize:
        tensor = ((tensor - tensor.min()) / (tensor.max() - tensor.min())) * (max_val - min_val) + min_val

    return tensor


def radialspace_2D(
        size: tuple[int] | tuple[int, int],
        curvy: float = 1.0,
        scale: float = 1.0,
        mode: str = "square",
        min_val: float = 0.0,
        max_val: float = 1.0,
        center: tuple[float, float] = (0.5, 0.5),
        function: Any = None,
        normalize: bool = True,
        dtype: dtype = torch.float32
) -> Tensor:
    """
    Create a 2D tensor with a radial gradient from 0 to 1 from the center to the edges.

    :param size: Tuple of int
        Size of the tensor.
        Can be a tuple of one or two integers.
        If one integer is given, the tensor will be square.
        If two integers are given, the tensor will have the given width and height.
    :param curvy: Float
        Curviness of the gradient.
        Higher values result in a sharper transition from 0 to 1.
    :param scale: Float
        Scale of the gradient.
        Higher values result in a larger area with values close to 1.
    :param mode: Str
        Shape of the gradient.
        Can be "square", "circle", "rectangle", or "corners".
    :param min_val: Float
        Minimum value in the tensor.
    :param max_val: Float
        Maximum value in the tensor.
    :param center: Tuple of float
        Coordinates of the center of the gradient.
    :param function: Callable or None
        Custom function for computing the distance from the center.
        If given, this function will be used instead of the built-in modes.
        The function should take two arguments (xx and yy) and return a tensor of the same shape.
    :param normalize: Bool
        Whether to normalize the tensor values to be between min_val and max_val.
    :param dtype: Torch.dtype
        Data type of the resulting tensor.

    :return: Torch.Tensor
        A 2D tensor with a radial gradient from 0 to 1 from the center to the edges.
    """
    if isinstance(size, tuple):
        if len(size) == 1:
            width = height = size[0]
        elif len(size) == 2:
            width, height = size
        else:
            raise ValueError("Invalid size argument")
    else:
        raise TypeError("Size must be a tuple")

    x = torch.linspace(0, 1, width)
    y = torch.linspace(0, 1, height)

    xx, yy = torch.meshgrid(x, y, indexing='ij')

    if function is not None:
        d = function(xx, yy)
    elif mode == "square":
        xx = (torch.abs(xx - center[0]) ** curvy)
        yy = (torch.abs(yy - center[1]) ** curvy)
        d = torch.max(xx, yy)
    elif mode == "circle":
        d = torch.sqrt((xx - center[0]) ** 2 + (yy - center[1]) ** 2)
        d = (d ** curvy)
    elif mode == "rectangle":
        xx = (torch.abs(xx - center[0]) ** curvy)
        yy = (torch.abs(yy - center[1]) ** curvy)
        d = xx + yy
    elif mode == "corners":
        xx = (torch.abs(xx - center[0]) ** curvy)
        yy = (torch.abs(yy - center[1]) ** curvy)
        d = torch.min(xx, yy)
    else:
        raise ValueError("Not supported mode.")

    if normalize:
        d = d / d.max() * scale
        d = torch.clamp(d, min_val, max_val)

    return d.to(dtype)


Tensor.tensor_to_image = tensor_to_image
ImageB.image_to_tensor = image_to_tensor
