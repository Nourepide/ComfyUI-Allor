class ClipClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip": ("CLIP",),
            },
        }

    RETURN_TYPES = ("CLIP",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, clip):
        return (clip,)


class ClipVisionClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip_vision": ("CLIP_VISION",),
            },
        }

    RETURN_TYPES = ("CLIP_VISION",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, clip_vision):
        return (clip_vision,)


class ClipVisionOutputClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip_vision_output": ("CLIP_VISION_OUTPUT",),
            },
        }

    RETURN_TYPES = ("CLIP_VISION_OUTPUT",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, clip_vision_output):
        return (clip_vision_output,)


class ConditioningClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, conditioning):
        return (conditioning,)


class ControlNetClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "control_net_clamp": ("CONTROL_NET",),
            },
        }

    RETURN_TYPES = ("CONTROL_NET",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, control_net_clamp):
        return (control_net_clamp,)


class GligenClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "gligen": ("GLIGEN",),
            },
        }

    RETURN_TYPES = ("GLIGEN",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, gligen):
        return (gligen,)


class ImageClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, image):
        return (image,)


class LatentClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent": ("LATENT",),
            },
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, latent):
        return (latent,)


class MaskClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
            },
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, mask):
        return (mask,)


class ModelClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
            },
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, model):
        return (model,)


class StyleModelClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "style_model": ("STYLE_MODEL",),
            },
        }

    RETURN_TYPES = ("STYLE_MODEL",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, style_model):
        return (style_model,)


class UpscaleModelClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "upscale_model": ("UPSCALE_MODEL",),
            },
        }

    RETURN_TYPES = ("UPSCALE_MODEL",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, upscale_model):
        return (upscale_model,)


class VaeClamp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "vae": ("VAE",),
            }
        }

    RETURN_TYPES = ("VAE",)
    FUNCTION = "node"
    CATEGORY = "clamp"

    def node(self, vae):
        return (vae,)


NODE_CLASS_MAPPINGS = {
    "ClipClamp": ClipClamp,
    "ClipVisionClamp": ClipVisionClamp,
    "ClipVisionOutputClamp": ClipVisionOutputClamp,
    "ConditioningClamp": ConditioningClamp,
    "ControlNetClamp": ControlNetClamp,
    "GligenClamp": GligenClamp,
    "ImageClamp": ImageClamp,
    "LatentClamp": LatentClamp,
    "MaskClamp": MaskClamp,
    "ModelClamp": ModelClamp,
    "StyleModelClamp": StyleModelClamp,
    "UpscaleModelClamp": UpscaleModelClamp,
    "VaeClamp": VaeClamp,
}
