from PIL import Image, ImageFont, ImageDraw
from rich import print
from shared.util import hex_to_rgb, rgb_to_rgba, crop_center

def draw_line(width: int, height: int,
            font_file: str, font_size: int,
            text: str, text_color: str, bg_color: str,
            x_offset: int, x_pos: str, y_offset: int, y_pos: int,
            opacity: float, accent: int | str, x_margin: int,
            angle: int, angle_x_pos: int, angle_y_pos: int, gradient_step: int
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

    total_words = round(((width - x_pos) // (text_size + x_margin))) + 1
    print(f"[bold cyan]TOTAL WORDS:[/bold cyan] {total_words}")
    print(f"[bold cyan]CENTER:[/bold cyan]      {total_words // 2}")

    if isinstance(accent, int) and accent < 0:
        accent = total_words + accent
    if accent == "gradient":
        opacity = gradient_step

    # Loop
    current_word = 0
    col = hex_to_rgb(text_color)
    transp_col = rgb_to_rgba(col, round(255 * opacity))
    accent_col = rgb_to_rgba(col, 255)

    while current_word < total_words:
        draw_col = transp_col
        if (accent != "off" and (current_word + 1) == accent) or (accent == "all"):
            draw_col = accent_col
        if accent == "gradient":
            if (current_word + 1) < (total_words // 2) and not opacity >= 1:
                opacity += gradient_step
            else:
                opacity -= gradient_step
            transp_col = rgb_to_rgba(col, round(255 * opacity))
            if (current_word + 1) == (total_words // 2):
                draw_col = accent_col
            if opacity > 1:
                opacity = 1
        image_FG_draw.text((render_x_pos, render_y_pos), text, fill=draw_col)

        render_x_pos += text_size + x_margin
        current_word += 1

    if angle != 0:
        image_FG = image_FG.rotate(angle, resample=Image.BICUBIC, expand=True)
        image_FG = crop_center(image_FG, width, height)

    image.paste(image_FG, (angle_x_pos, angle_y_pos))
    image_BG.paste(image, mask=image)

    return image_BG
