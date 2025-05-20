from PIL import Image, ImageFont, ImageDraw

# --- Modify this constants to your likings

RESOLUTION = (2560, 1440)
RESOLUTION_FG = (RESOLUTION[0] * 2, RESOLUTION[1] * 2)
FONT = ImageFont.truetype("./fonts/BebasNeue/Bebas_Neue_Regular.ttf", 72)
TEXT = "HELLO, WORLD! "
TEXT_COLOR = "#ffffff"
BG_COLOR = "#000000"
ANGLE = 15

# --- Line Gen Code

image = Image.new("RGBA", RESOLUTION, (0, 0, 0, 0))
image_BG = Image.new("RGBA", RESOLUTION, BG_COLOR)
image_FG = Image.new("RGBA", RESOLUTION_FG, (0, 0, 0, 0))

image_FG_draw = ImageDraw.Draw(image_FG)
image_FG_draw.font = FONT
image_FG_draw.fontmode = "L"

text_size = image_FG_draw.textlength(TEXT)
render_x_offset = -16  # set offset of the start
render_y_offset = 0  # set offset of the start
render_x_pos = 0 + render_x_offset  # set start x pos
render_y_pos = 0 + render_y_offset  # set y pos

total_words = round((RESOLUTION_FG[0] / (text_size + 4))) + 1
total_lines = round((RESOLUTION_FG[1] / 64)) + 1
accent_line = total_lines - (round(16 * 1.4))  # set which line will be highlighted as a full solid color
current_line = 0
current_word = 0


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_rgba(value, alpha):
    return tuple([value[0], value[1], value[2], alpha])


col = hex_to_rgb(TEXT_COLOR)

transp_col = rgb_to_rgba(col, round(255 * 0.25))
accent_col = rgb_to_rgba(col, 255)

while current_line < total_lines:
    col = transp_col
    if current_line == accent_line:
        col = accent_col

    while current_word < total_words:
        image_FG_draw.text((render_x_pos, render_y_pos), TEXT, fill=col)

        render_x_pos += text_size + 4
        current_word += 1

    render_x_pos = 0 + (render_x_offset * current_line)
    current_word = 0
    render_y_pos += 64
    current_line += 1


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(
        (
            (img_width - crop_width) // 2,
            (img_height - crop_height) // 2,
            (img_width + crop_width) // 2,
            (img_height + crop_height) // 2,
        )
    )


image_FG = image_FG.rotate(ANGLE, expand=1)
image_FG = crop_center(image_FG, RESOLUTION[0], RESOLUTION[1])

image.paste(image_FG, (0, 0))
image = Image.alpha_composite(image_BG, image_FG)
image.show()
image.save("./image.png")
