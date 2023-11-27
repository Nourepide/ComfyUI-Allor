from PIL import Image, ImageDraw, ImageFont

import folder_paths


class ImageText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": False}),
                "font": (folder_paths.get_filename_list("fonts"),),
                "size": ("INT", {
                    "default": 28,
                    "min": 1,
                    "step": 1
                }),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 1.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "margin_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "margin_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/draw"

    def node(self, text, font, size, red, green, blue, alpha, margin_x, margin_y):
        outline_size = 0
        outline_red = 255
        outline_green = 255
        outline_blue = 255

        return ImageTextOutlined().node(
            text,
            font,
            size,
            red,
            green,
            blue,
            outline_size,
            outline_red,
            outline_green,
            outline_blue,
            alpha,
            margin_x,
            margin_y
        )


class ImageTextOutlined:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": False}),
                "font": (folder_paths.get_filename_list("fonts"),),
                "size": ("INT", {
                    "default": 28,
                    "min": 1,
                    "step": 1
                }),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "outline_size": ("INT", {
                    "default": 1,
                    "step": 1
                }),
                "outline_red": ("INT", {
                    "default": 0,
                    "max": 255,
                    "step": 1
                }),
                "outline_green": ("INT", {
                    "default": 0,
                    "max": 255,
                    "step": 1
                }),
                "outline_blue": ("INT", {
                    "default": 0,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 1.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "margin_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "margin_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/draw"

    def node(
            self, text, font, size, red, green, blue, outline_size, outline_red, outline_green, outline_blue, alpha,
            margin_x, margin_y
    ):
        font_path = folder_paths.get_full_path("fonts", font)
        font = ImageFont.truetype(font_path, size, encoding="unic")

        (left, top, right, bottom) = font.getbbox(text)

        canvas = Image.new("RGBA", (
            right + (margin_x + outline_size) * 2,
            bottom - top + (margin_y + outline_size) * 2
        ), (0, 0, 0, 0))

        draw = ImageDraw.Draw(canvas)

        draw.text(
            (margin_x + outline_size, margin_y + outline_size - top),
            text=text, fill=(red, green, blue, int(alpha * 255)),
            stroke_fill=(outline_red, outline_green, outline_blue, int(alpha * 255)),
            stroke_width=outline_size, font=font
        )

        return (canvas.image_to_tensor().unsqueeze(0),)


class ImageTextMultiline:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "font": (folder_paths.get_filename_list("fonts"),),
                "align": (["left", "center", "right"],),
                "size": ("INT", {
                    "default": 28,
                    "min": 1,
                    "step": 1
                }),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 1.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "margin_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "margin_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/draw"

    def node(self, text, font, align, size, red, green, blue, alpha, margin_x, margin_y):
        outline_size = 0
        outline_red = 255
        outline_green = 255
        outline_blue = 255

        return ImageTextMultilineOutlined().node(
            text,
            font,
            align,
            size,
            red,
            green,
            blue,
            outline_size,
            outline_red,
            outline_green,
            outline_blue,
            alpha,
            margin_x,
            margin_y
        )


class ImageTextMultilineOutlined:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "font": (folder_paths.get_filename_list("fonts"),),
                "align": (["left", "center", "right"],),
                "size": ("INT", {
                    "default": 28,
                    "min": 1,
                    "step": 1
                }),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "outline_size": ("INT", {
                    "default": 1,
                    "step": 1
                }),
                "outline_red": ("INT", {
                    "default": 0,
                    "max": 255,
                    "step": 1
                }),
                "outline_green": ("INT", {
                    "default": 0,
                    "max": 255,
                    "step": 1
                }),
                "outline_blue": ("INT", {
                    "default": 0,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 1.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "margin_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "margin_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/draw"

    def node(
            self, text, font, align, size, red, green, blue, outline_size, outline_red, outline_green, outline_blue,
            alpha, margin_x, margin_y
    ):
        font_path = folder_paths.get_full_path("fonts", font)
        font = ImageFont.truetype(font_path, size, encoding="unic")

        lines = text.split('\n').__len__()
        (_, top, _, _) = font.getbbox(text)

        canvas = Image.new("RGBA", (0, 0))
        draw = ImageDraw.Draw(canvas)
        text_size = draw.multiline_textbbox((0, 0), text, font)

        canvas = Image.new("RGBA", (
            text_size[2] + (margin_x + outline_size) * 2,
            text_size[3] - top + (margin_y + (outline_size * lines)) * 2
        ), (0, 0, 0, 0))

        draw = ImageDraw.Draw(canvas)

        draw.text(
            (margin_x + outline_size, margin_y + outline_size - top),
            text=text, fill=(red, green, blue, int(alpha * 255)),
            stroke_fill=(outline_red, outline_green, outline_blue, int(alpha * 255)),
            stroke_width=outline_size, font=font, align=align
        )

        return (canvas.image_to_tensor().unsqueeze(0),)


NODE_CLASS_MAPPINGS = {
    "ImageText": ImageText,
    "ImageTextOutlined": ImageTextOutlined,
    "ImageTextMultiline": ImageTextMultiline,
    "ImageTextMultilineOutlined": ImageTextMultilineOutlined
}
