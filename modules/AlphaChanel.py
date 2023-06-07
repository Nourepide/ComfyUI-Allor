import torch


class AlphaChanelByMask:
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
    FUNCTION = "alpha_chanel_by_mask"
    CATEGORY = "mask/alpha"

    def alpha_chanel_by_mask(self, images, mask, method):
        img_height, img_width = images[0, :, :, 0].shape
        mask_height, mask_width = mask.shape

        if img_height != mask_height or img_width != mask_width:
            raise ValueError(
                "[AlphaChanelByMask]: Size of images not equals size of mask. " +
                "Images: [" + str(img_width) + ", " + str(img_height) + "] - " +
                "Mask: [" + str(mask_width) + ", " + str(mask_height) + "]."
            )

        if method == "default":
            return (torch.stack([
                torch.stack((
                    images[i, :, :, 0],
                    images[i, :, :, 1],
                    images[i, :, :, 2],
                    1. - mask
                ), dim=-1) for i in range(len(images))
            ]),)
        else:
            return (torch.stack([
                torch.stack((
                    images[i, :, :, 0],
                    images[i, :, :, 1],
                    images[i, :, :, 2],
                    mask
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
    FUNCTION = "alpha_chanel_as_mask"
    CATEGORY = "mask/alpha"

    def alpha_chanel_as_mask(self, images, method):
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
                "method": (["default", "only_add", "only_restore"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "alpha_chanel_restore"
    CATEGORY = "mask/alpha"

    def alpha_chanel_restore(self, images, method):
        dimensions = images[0, 0, 0, :].shape[0]
        width, height = images[0, :, :, 0].shape

        alpha = torch.ones((width, height))

        def add():
            return (torch.stack([
                torch.stack((
                    images[i, :, :, 0],
                    images[i, :, :, 1],
                    images[i, :, :, 2],
                    alpha
                ), dim=-1) for i in range(len(images))
            ]),)

        def restore():
            images[:, :, :, 3] = alpha
            return (images,)

        if method == "default":
            return add() if dimensions != 4 else restore()
        elif method == "only_add":
            return add() if dimensions != 4 else (images,)
        else:
            return restore() if dimensions == 4 else (images,)


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
    FUNCTION = "alpha_chanel_remove"
    CATEGORY = "mask/alpha"

    def alpha_chanel_remove(self, images):
        return (torch.stack([
            torch.stack((
                images[i, :, :, 0],
                images[i, :, :, 1],
                images[i, :, :, 2]
            ), dim=-1) for i in range(len(images))
        ]),)


NODE_CLASS_MAPPINGS = {
    "AlphaChanelByMask": AlphaChanelByMask,
    "AlphaChanelAsMask": AlphaChanelAsMask,
    "AlphaChanelRestore": AlphaChanelRestore,
    "AlphaChanelRemove": AlphaChanelRemove
}
