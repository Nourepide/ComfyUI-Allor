import numpy as np
import torch


def channels_layer(images, channels, function):
    if channels == "rgb":
        img = images[:, :, :, :3]
    elif channels == "rgba":
        img = images[:, :, :, :4]
    elif channels == "rg":
        img = images[:, :, :, [0, 1]]
    elif channels == "rb":
        img = images[:, :, :, [0, 2]]
    elif channels == "ra":
        img = images[:, :, :, [0, 3]]
    elif channels == "gb":
        img = images[:, :, :, [1, 2]]
    elif channels == "ga":
        img = images[:, :, :, [1, 3]]
    elif channels == "ba":
        img = images[:, :, :, [2, 3]]
    elif channels == "r":
        img = images[:, :, :, 0]
    elif channels == "g":
        img = images[:, :, :, 1]
    elif channels == "b":
        img = images[:, :, :, 2]
    elif channels == "a":
        img = images[:, :, :, 3]
    else:
        raise ValueError("Unsupported channels")

    result = torch.from_numpy(function(img.numpy()))

    if channels == "rgb":
        images[:, :, :, :3] = result
    elif channels == "rgba":
        images[:, :, :, :4] = result
    elif channels == "rg":
        images[:, :, :, [0, 1]] = result
    elif channels == "rb":
        images[:, :, :, [0, 2]] = result
    elif channels == "ra":
        images[:, :, :, [0, 3]] = result
    elif channels == "gb":
        images[:, :, :, [1, 2]] = result
    elif channels == "ga":
        images[:, :, :, [1, 3]] = result
    elif channels == "ba":
        images[:, :, :, [2, 3]] = result
    elif channels == "r":
        images[:, :, :, 0] = result
    elif channels == "g":
        images[:, :, :, 1] = result
    elif channels == "b":
        images[:, :, :, 2] = result
    elif channels == "a":
        images[:, :, :, 3] = result

    return images


class ImageNoiseBeta:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "a": ("INT", {
                    "default": 1,
                    "min": 1,
                }),
                "b": ("INT", {
                    "default": 1,
                    "min": 1,
                }),
                "monochromatic": (["false", "true"],),
                "invert": (["false", "true"],),
                "channels": (["rgb", "rgba", "rg", "rb", "ra", "gb", "ga", "ba", "r", "g", "b", "a"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/noise"

    def noise(self, images, a, b, monochromatic, invert):
        if monochromatic and images.shape[3] > 1:
            noise = np.random.beta(a, b, images.shape[:3])
        else:
            noise = np.random.beta(a, b, images.shape)

        if monochromatic and images.shape[3] > 1:
            noise = noise[..., np.newaxis].repeat(images.shape[3], -1)

        if invert:
            noise = images - noise
        else:
            noise = images + noise

        noise = noise.astype(images.dtype)

        return noise

    def node(self, images, a, b, monochromatic, invert, channels):
        tensor = images.clone().detach()

        monochromatic = True if monochromatic == "true" else False
        invert = True if invert == "true" else False

        return (channels_layer(tensor, channels, lambda x: self.noise(
            x, a, b, monochromatic, invert
        )),)


class ImageNoiseBinomial:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "n": ("INT", {
                    "default": 128,
                    "min": 1,
                    "max": 255,
                }),
                "p": ("FLOAT", {
                    "default": 0.5,
                    "max": 1.0,
                    "step": 0.01
                }),
                "monochromatic": (["false", "true"],),
                "invert": (["false", "true"],),
                "channels": (["rgb", "rgba", "rg", "rb", "ra", "gb", "ga", "ba", "r", "g", "b", "a"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/noise"

    def noise(self, images, n, p, monochromatic, invert):
        if monochromatic and images.shape[3] > 1:
            noise = np.random.binomial(n, p, images.shape[:3])
        else:
            noise = np.random.binomial(n, p, images.shape)

        noise = noise.astype(images.dtype)
        noise /= 255

        if monochromatic and images.shape[3] > 1:
            noise = noise[..., np.newaxis].repeat(images.shape[3], -1)

        if invert:
            noise = images - noise
        else:
            noise = images + noise

        noise = np.clip(noise, 0.0, 1.0)

        return noise

    def node(self, images, n, p, monochromatic, invert, channels):
        tensor = images.clone().detach()

        monochromatic = True if monochromatic == "true" else False
        invert = True if invert == "true" else False

        return (channels_layer(tensor, channels, lambda x: self.noise(
            x, n, p, monochromatic, invert
        )),)


class ImageNoiseBytes:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "monochromatic": (["false", "true"],),
                "invert": (["false", "true"],),
                "channels": (["rgb", "rgba", "rg", "rb", "ra", "gb", "ga", "ba", "r", "g", "b", "a"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/noise"

    def noise(self, images, monochromatic, invert):
        if monochromatic and images.shape[3] > 1:
            noise = np.random.bytes(np.prod(images.shape[:3]))
            noise = np.frombuffer(noise, np.uint8)
            noise = np.reshape(noise, images.shape[:3])
        else:
            noise = np.random.bytes(np.prod(images.shape))
            noise = np.frombuffer(noise, np.uint8)
            noise = np.reshape(noise, images.shape)

        noise = noise.astype(images.dtype)
        noise /= 255

        if monochromatic and images.shape[3] > 1:
            noise = noise[..., np.newaxis].repeat(images.shape[3], -1)

        if invert:
            noise = images - noise
        else:
            noise = images + noise

        noise = np.clip(noise, 0.0, 1.0)

        return noise

    def node(self, images, monochromatic, invert, channels):
        tensor = images.clone().detach()

        monochromatic = True if monochromatic == "true" else False
        invert = True if invert == "true" else False

        return (channels_layer(tensor, channels, lambda x: self.noise(
            x, monochromatic, invert
        )),)


class ImageNoiseGaussian:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "strength": ("FLOAT", {
                    "default": 0.5,
                    "step": 0.01
                }),
                "monochromatic": (["false", "true"],),
                "invert": (["false", "true"],),
                "channels": (["rgb", "rgba", "rg", "rb", "ra", "gb", "ga", "ba", "r", "g", "b", "a"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/noise"

    def noise(self, images, strength, monochromatic, invert):
        if monochromatic and images.shape[3] > 1:
            noise = np.random.normal(0, 1, images.shape[:3])
        else:
            noise = np.random.normal(0, 1, images.shape)

        noise = np.abs(noise)
        noise /= noise.max()

        if monochromatic and images.shape[3] > 1:
            noise = noise[..., np.newaxis].repeat(images.shape[3], -1)

        if invert:
            noise = images - noise * strength
        else:
            noise = images + noise * strength

        noise = np.clip(noise, 0.0, 1.0)
        noise = noise.astype(images.dtype)

        return noise

    def node(self, images, strength, monochromatic, invert, channels):
        tensor = images.clone().detach()

        monochromatic = True if monochromatic == "true" else False
        invert = True if invert == "true" else False

        return (channels_layer(tensor, channels, lambda x: self.noise(
            x, strength, monochromatic, invert
        )),)


NODE_CLASS_MAPPINGS = {
    "ImageNoiseBeta": ImageNoiseBeta,
    "ImageNoiseBinomial": ImageNoiseBinomial,
    "ImageNoiseBytes": ImageNoiseBytes,
    "ImageNoiseGaussian": ImageNoiseGaussian
}
