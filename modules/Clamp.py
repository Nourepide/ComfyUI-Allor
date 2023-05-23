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
    FUNCTION = "clip_clamp"
    CATEGORY = "clamp"

    def clip_clamp(self, clip):
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
    FUNCTION = "clip_vision_clamp"
    CATEGORY = "clamp"

    def clip_vision_clamp(self, clip_vision):
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
    FUNCTION = "clip_vision_output_clamp"
    CATEGORY = "clamp"

    def clip_vision_output_clamp(self, clip_vision_output):
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
    FUNCTION = "conditioning_clamp"
    CATEGORY = "clamp"

    def conditioning_clamp(self, conditioning):
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
    FUNCTION = "control_net_clamp"
    CATEGORY = "clamp"

    def control_net_clamp(self, control_net_clamp):
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
    FUNCTION = "gligen_clamp"
    CATEGORY = "clamp"

    def gligen_clamp(self, gligen):
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
    FUNCTION = "image_clamp"
    CATEGORY = "clamp"

    def image_clamp(self, image):
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
    FUNCTION = "latent_clamp"
    CATEGORY = "clamp"

    def latent_clamp(self, latent):
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
    FUNCTION = "mask_clamp"
    CATEGORY = "clamp"

    def mask_clamp(self, mask):
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
    FUNCTION = "model_clamp"
    CATEGORY = "clamp"

    def model_clamp(self, model):
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
    FUNCTION = "style_mode_clamp"
    CATEGORY = "clamp"

    def style_mode_clamp(self, style_model):
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
    FUNCTION = "upscale_mode_clamp"
    CATEGORY = "clamp"

    def upscale_mode_clamp(self, upscale_model):
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
    FUNCTION = "vae_clamp"
    CATEGORY = "clamp"

    def vae_clamp(self, vae):
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
