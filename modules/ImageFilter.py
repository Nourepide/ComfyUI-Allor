import torch
from PIL import ImageFilter


def applyImageFilter(images, image_filter):
    return (torch.stack([
        images[i].tensor_to_image().filter(image_filter).image_to_tensor() for i in range(len(images))
    ]),)


class ImageFilterSmooth:
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
    FUNCTION = "image_filter_smooth"
    CATEGORY = "image/filter"

    def image_filter_smooth(self, images):
        return applyImageFilter(images, ImageFilter.SMOOTH)


class ImageFilterSmoothMore:
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
    FUNCTION = "image_filter_smooth_more"
    CATEGORY = "image/filter"

    def image_filter_smooth_more(self, images):
        return applyImageFilter(images, ImageFilter.SMOOTH_MORE)


class ImageFilterBlur:
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
    FUNCTION = "image_filter_blur"
    CATEGORY = "image/filter"

    def image_filter_blur(self, images):
        return applyImageFilter(images, ImageFilter.BLUR)


class ImageFilterBoxBlur:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "radius": ("INT", {
                    "default": 1,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_filter_box_blur"
    CATEGORY = "image/filter"

    def image_filter_box_blur(self, images, radius):
        return applyImageFilter(images, ImageFilter.BoxBlur(radius))


class ImageFilterGaussianBlur:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "radius": ("INT", {
                    "default": 1,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_filter_gaussian_blur"
    CATEGORY = "image/filter"

    def image_filter_gaussian_blur(self, images, radius):
        return applyImageFilter(images, ImageFilter.GaussianBlur(radius))


class ImageFilterContour:
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
    FUNCTION = "image_filter_contour"
    CATEGORY = "image/filter"

    def image_filter_contour(self, images):
        return applyImageFilter(images, ImageFilter.CONTOUR)


class ImageFilterDetail:
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
    FUNCTION = "image_filter_detail"
    CATEGORY = "image/filter"

    def image_filter_detail(self, images):
        return applyImageFilter(images, ImageFilter.DETAIL)


class ImageFilterEdgeEnhance:
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
    FUNCTION = "image_filter_edge_enhance"
    CATEGORY = "image/filter"

    def image_filter_edge_enhance(self, images):
        return applyImageFilter(images, ImageFilter.EDGE_ENHANCE)


class ImageFilterEdgeEnhanceMore:
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
    FUNCTION = "image_filter_edge_enhance_more"
    CATEGORY = "image/filter"

    def image_filter_edge_enhance_more(self, images):
        return applyImageFilter(images, ImageFilter.EDGE_ENHANCE_MORE)


class ImageFilterEmboss:
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
    FUNCTION = "image_filter_emboss"
    CATEGORY = "image/filter"

    def image_filter_emboss(self, images):
        return applyImageFilter(images, ImageFilter.EMBOSS)


class ImageFilterFindEdges:
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
    FUNCTION = "image_filter_find_edges"
    CATEGORY = "image/filter"

    def image_filter_find_edges(self, images):
        return applyImageFilter(images, ImageFilter.FIND_EDGES)


class ImageFilterSharpen:
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
    FUNCTION = "image_filter_sharpen"
    CATEGORY = "image/filter"

    def image_filter_sharpen(self, images):
        return applyImageFilter(images, ImageFilter.SHARPEN)


class ImageFilterRank:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "size": ("INT", {
                    "default": 2,
                    "min": 0,
                    "step": 2
                }),
                "rank": ("INT", {
                    "default": 1,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_filter_rank"
    CATEGORY = "image/filter"

    def image_filter_rank(self, images, size, rank):
        return applyImageFilter(images, ImageFilter.RankFilter(int(size) + 1, rank))


class ImageFilterMedian:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "size": ("INT", {
                    "default": 2,
                    "min": 0,
                    "step": 2
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_filter_median"
    CATEGORY = "image/filter"

    def image_filter_median(self, images, size):
        return applyImageFilter(images, ImageFilter.MedianFilter(int(size) + 1))


class ImageFilterMin:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "size": ("INT", {
                    "default": 2,
                    "min": 0,
                    "step": 2
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_filter_min"
    CATEGORY = "image/filter"

    def image_filter_min(self, images, size):
        return applyImageFilter(images, ImageFilter.MinFilter(int(size) + 1))


class ImageFilterMax:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "size": ("INT", {
                    "default": 2,
                    "min": 0,
                    "step": 2
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_filter_max"
    CATEGORY = "image/filter"

    def image_filter_max(self, images, size):
        return applyImageFilter(images, ImageFilter.MaxFilter(int(size) + 1))


class ImageFilterMode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "size": ("INT", {
                    "default": 2,
                    "min": 0,
                    "step": 2
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_filter_mode"
    CATEGORY = "image/filter"

    def image_filter_mode(self, images, size):
        return applyImageFilter(images, ImageFilter.ModeFilter(int(size) + 1))


NODE_CLASS_MAPPINGS = {
    "ImageFilterSmooth": ImageFilterSmooth,
    "ImageFilterSmoothMore": ImageFilterSmoothMore,
    "ImageFilterBlur": ImageFilterBlur,
    "ImageFilterBoxBlur": ImageFilterBoxBlur,
    "ImageFilterGaussianBlur": ImageFilterGaussianBlur,
    "ImageFilterContour": ImageFilterContour,
    "ImageFilterDetail": ImageFilterDetail,
    "ImageFilterEdgeEnhance": ImageFilterEdgeEnhance,
    "ImageFilterEdgeEnhanceMore": ImageFilterEdgeEnhanceMore,
    "ImageFilterEmboss": ImageFilterEmboss,
    "ImageFilterFindEdges": ImageFilterFindEdges,
    "ImageFilterSharpen": ImageFilterSharpen,
    "ImageFilterRank": ImageFilterRank,
    "ImageFilterMedian": ImageFilterMedian,
    "ImageFilterMin": ImageFilterMin,
    "ImageFilterMax": ImageFilterMax,
    "ImageFilterMode": ImageFilterMode
}
