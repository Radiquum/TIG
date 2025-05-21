from PIL import Image, ImageFont, ImageDraw
from rich import print
from shared.util import hex_to_rgb, rgb_to_rgba, generate_random_symbols

def draw_fill(width: int, height: int,
            font_file: str, font_size: int,
            text: str, text_color: str, bg_color: str,
            x_offset: int, x_pos: str, y_offset: int, y_pos: int,
            opacity: float, accent: int, x_margin: int, y_margin: int,
            preview_only: bool
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
    total_lines = round(((height - y_pos) // (font_size + y_margin))) + 2
    print(f"[bold cyan]TOTAL WORDS IN LINE:[/bold cyan] {total_words}")
    print(f"[bold cyan]TOTAL LINES:[/bold cyan] {(total_lines - 1)}")
    print(f"[bold cyan]CENTER:[/bold cyan]      {(total_lines - 1) // 2}")

    if accent < 0:
        accent = total_lines + accent

    # Loop
    current_word = 0
    current_line = 1
    col = hex_to_rgb(text_color)
    transp_col = rgb_to_rgba(col, round(255 * opacity))
    accent_col = rgb_to_rgba(col, 255)

    while current_line < total_lines:
        col = transp_col
        if current_line == accent:
            col = accent_col

        while current_word < total_words:
            image_FG_draw.text((render_x_pos, render_y_pos), text, fill=col)

            render_x_pos += text_size + x_margin
            current_word += 1

        render_x_pos = x_pos + (x_offset * current_line)
        current_word = 0
        render_y_pos += font_size + y_margin
        current_line += 1

    image.paste(image_FG)
    image = Image.alpha_composite(image_BG, image_FG)

    image.show()
    if not preview_only:
        image.save(f"line_{width}x{height}_fg-{text_color[1:]}_bg-{bg_color[1:]}_{generate_random_symbols(6)}.png")
