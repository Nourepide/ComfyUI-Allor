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


Tensor.tensor_to_image = tensor_to_image
ImageB.image_to_tensor = image_to_tensor
