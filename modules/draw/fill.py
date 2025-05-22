from PIL import Image, ImageFont, ImageDraw, ImageOps
from rich import print
from shared.util import hex_to_rgb, rgb_to_rgba, crop_center


def draw_fill(
    width: int,
    height: int,
    font_file: str,
    font_size: int,
    text: str,
    text_color: str,
    bg_color: str,
    x_offset: int,
    x_pos: str,
    y_offset: int,
    y_pos: int,
    opacity: float,
    accent: int | str,
    x_margin: int,
    y_margin: int,
    angle: int,
):
    RESOLUTION = (width, height)
    FONT = ImageFont.truetype(font_file, font_size)

    image = Image.new("RGBA", RESOLUTION, (0, 0, 0, 0))
    image_BG = Image.new("RGBA", RESOLUTION, bg_color)
    image_FG = Image.new("RGBA", RESOLUTION, (0, 0, 0, 0))

    image_FG_draw = ImageDraw.Draw(image_FG)
    image_FG_draw.font = FONT
    image_FG_draw.fontmode = "L"

    text_size = image_FG_draw.textlength(text)

    if x_pos < 0:
        x_pos = width + x_pos
    render_x_pos = x_pos + x_offset

    if y_pos < 0:
        y_pos = height + y_pos
    render_y_pos = y_pos + y_offset

    total_words = round(((width - x_pos) // (text_size + x_margin))) + 2
    total_lines = round(((height - y_pos) // (font_size + y_margin))) + 2
    if isinstance(accent, int) and accent < 0:
        accent = total_words + accent

    if angle != 0:
        total_lines = round(total_lines * 2)
        total_words = round(total_words * 2)
        image_FG = ImageOps.expand(
            image_FG, (0, 0, round(width), round(height)), (0, 0, 0, 0)
        )
        image_FG_draw = ImageDraw.Draw(image_FG)
        image_FG_draw.font = FONT
        image_FG_draw.fontmode = "L"

    print(f"[bold cyan]TOTAL LINES:[/bold cyan] {(total_lines - 1 - 2)}")
    print(f"[bold cyan]CENTER:[/bold cyan]      {(total_lines - 1) // 2}")

    # Loop
    current_word = 0
    current_line = 1
    col = hex_to_rgb(text_color)
    transp_col = rgb_to_rgba(col, round(255 * opacity))
    accent_col = rgb_to_rgba(col, 255)

    while current_line < total_lines:
        col = transp_col
        if (accent != "off" and current_line == accent) or (accent == "all"):
            col = accent_col

        while current_word < total_words:
            image_FG_draw.text((render_x_pos, render_y_pos), text, fill=col)

            render_x_pos += text_size + x_margin
            current_word += 1

        render_x_pos = x_pos + (x_offset * current_line)
        current_word = 0
        render_y_pos += font_size + y_margin
        current_line += 1

    if angle != 0:
        image_FG = image_FG.rotate(angle, resample=Image.BICUBIC, expand=True)
        image_FG = crop_center(image_FG, width, height)

    image.paste(image_FG)
    image = Image.alpha_composite(image_BG, image_FG)

    return image
