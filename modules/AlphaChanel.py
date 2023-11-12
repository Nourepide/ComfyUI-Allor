import torch


class AlphaChanelAdd:
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
    CATEGORY = "image/alpha"

    def node(self, images):
        batch, height, width, channels = images.shape

        if channels == 4:
            return images

        alpha = torch.ones((batch, height, width, 1))

        return (torch.cat((images, alpha), dim=-1),)


class AlphaChanelAddByMask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "mask": ("MASK",),
                "method": (["default", "invert"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/alpha"

    def node(self, images, mask, method):
        img_count, img_height, img_width = images[:, :, :, 0].shape
        mask_count, mask_height, mask_width = mask.shape

        if mask_width == 64 and mask_height == 64:
            mask = torch.zeros((img_count, img_height, img_width))
        else:
            if img_height != mask_height or img_width != mask_width:
                raise ValueError(
                    "[AlphaChanelByMask]: Size of images not equals size of mask. " +
                    "Images: [" + str(img_width) + ", " + str(img_height) + "] - " +
                    "Mask: [" + str(mask_width) + ", " + str(mask_height) + "]."
                )

        if img_count != mask_count:
            mask = mask.expand((img_count, -1, -1))

        if method == "default":
            return (torch.stack([
                torch.stack((
                    images[i, :, :, 0],
                    images[i, :, :, 1],
                    images[i, :, :, 2],
                    1. - mask[i]
                ), dim=-1) for i in range(len(images))
            ]),)
        else:
            return (torch.stack([
                torch.stack((
                    images[i, :, :, 0],
                    images[i, :, :, 1],
                    images[i, :, :, 2],
                    mask[i]
                ), dim=-1) for i in range(len(images))
            ]),)


class AlphaChanelAsMask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "method": (["default", "invert"],),
            },
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "node"
    CATEGORY = "image/alpha"

    def node(self, images, method):
        if images[0, 0, 0].shape[0] != 4:
            raise ValueError("Alpha chanel not exist.")

        if method == "default":
            return (1.0 - images[0, :, :, 3],)
        elif method == "invert":
            return (images[0, :, :, 3],)
        else:
            raise ValueError("Unexpected method.")


class AlphaChanelRestore:
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
    CATEGORY = "image/alpha"

    def node(self, images):
        batch, height, width, channels = images.shape

        if channels != 4:
            return images

        tensor = images.clone().detach()

        tensor[:, :, :, 3] = torch.ones((batch, height, width))

        return (tensor,)


class AlphaChanelRemove:
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
    CATEGORY = "image/alpha"

    def node(self, images):
        return (images[:, :, :, 0:3],)


NODE_CLASS_MAPPINGS = {
    "AlphaChanelAdd": AlphaChanelAdd,
    "AlphaChanelAddByMask": AlphaChanelAddByMask,
    "AlphaChanelAsMask": AlphaChanelAsMask,
    "AlphaChanelRestore": AlphaChanelRestore,
    "AlphaChanelRemove": AlphaChanelRemove
}
