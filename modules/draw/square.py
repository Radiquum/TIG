from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageOps
from shared.util import hex_to_rgb
from shared.log import log
from sys import exit

def draw_square(
    width: int,
    height: int,
    font_file: str,
    font_size: int,
    text: str,
    text_color: str,
    bg_color: str,
    x_pos: str,
    y_pos: int,
    opacity: float,
    accent: int | str,
    x_margin: int,
    y_margin: int,
    border: tuple[int,int]
):
    RESOLUTION = (width, height)
    FONT = ImageFont.truetype(font_file, font_size)

    image = Image.new("RGBA", RESOLUTION, (0, 0, 0, 0))
    image_BG = Image.new("RGBA", RESOLUTION, bg_color)
    image_FG = Image.new("RGBA", RESOLUTION, (0, 0, 0, 0))

    image_FG_draw = ImageDraw.Draw(image_FG)
    image_FG_draw.font = FONT
    image_FG_draw.fontmode = "L"

    text_box = image_FG_draw.textbbox((0, 0), text)

    if x_pos < 0:
        x_pos = width + x_pos
    render_x_pos = x_pos + x_margin

    if y_pos < 0:
        y_pos = height + y_pos
    render_y_pos = y_pos + x_margin

    col = hex_to_rgb(text_color)

    image_TEXT = Image.new(
        "RGBA", (text_box[2], text_box[3] - text_box[1]), (0, 0, 0, 0)
    )
    image_TEXT_draw = ImageDraw.Draw(image_TEXT)
    image_TEXT_draw.font = FONT
    image_TEXT_draw.fontmode = "L"
    image_TEXT_draw.text((0, -text_box[1]), text, col)

    image_TEXT_90 = image_TEXT.rotate(90, resample=Image.BICUBIC, expand=True)
    image_TEXT_180 = image_TEXT.rotate(180, resample=Image.BICUBIC, expand=True)
    image_TEXT_270 = image_TEXT.rotate(270, resample=Image.BICUBIC, expand=True)

    image_TEXT_Combine = Image.new(
        "RGBA",
        (image_TEXT.width, (image_TEXT_90.height + (image_TEXT.height * 2))),
        (0, 0, 0, 0),
    )
    image_TEXT_Combine.paste(image_TEXT, (0, 0))
    image_TEXT_Combine.paste(image_TEXT_90, (0, image_TEXT.height))
    image_TEXT_Combine.paste(
        image_TEXT_180, (0, image_TEXT.height + image_TEXT_90.height)
    )
    image_TEXT_Combine.paste(
        image_TEXT_270,
        (image_TEXT_Combine.width - image_TEXT_270.width, image_TEXT.height),
    )

    total_x_lines = (image_FG.width // image_TEXT_Combine.width) + 1
    total_y_lines = (image_FG.height // image_TEXT_Combine.height) + 1

    accent_x = 0
    accent_y = 0

    if accent == "gradient":
        log.error("Gradient accent is not supported for this mode")
        exit(1)

    if accent not in ["off", "all"]:
        accent_x = accent
        accent_y = accent // 2
        if accent < 0:
            accent_x = total_x_lines + accent
            accent_y = total_y_lines + (accent // 2)

    for y in range(total_y_lines):
        for x in range(total_x_lines):
            TEXT_LAYER_COPY = image_TEXT_Combine.copy()

            if y != (accent_y - 1) and x != (accent_x - 1):
                if accent == "all":
                    opacity = 1

                alpha = TEXT_LAYER_COPY.split()[3]
                alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
                TEXT_LAYER_COPY.putalpha(alpha)

            image_FG.paste(TEXT_LAYER_COPY, (render_x_pos, render_y_pos))
            render_x_pos += image_TEXT_Combine.width + x_margin
        render_x_pos = x_margin
        render_y_pos += image_TEXT_Combine.height + y_margin

    image.paste(image_FG, (0, 0))
    image_BG.paste(image, mask=image)

    if border and border[0] != 0:
        image_BG = image_BG.crop((border[0], border[1], image_BG.width - border[0], image_BG.height - border[1]))
        image_BG = ImageOps.expand(image_BG, (border[0], border[1]), fill=bg_color)

    return image_BG
