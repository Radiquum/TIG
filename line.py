from PIL import Image, ImageFont, ImageDraw

# --- Modify this constants to your likings

RESOLUTION = (2560, 1440)
FONT = ImageFont.truetype("./fonts/BebasNeue/Bebas_Neue_Regular.ttf", 72)
TEXT = "HELLO, WORLD! "
TEXT_COLOR = "#ffffff"
BG_COLOR = "#000000"

# --- Line Gen Code

image = Image.new("RGBA", RESOLUTION, (0, 0, 0, 0))
image_BG = Image.new("RGBA", RESOLUTION, BG_COLOR)
image_FG = Image.new("RGBA", RESOLUTION, (0, 0, 0, 0))

image_FG_draw = ImageDraw.Draw(image_FG)
image_FG_draw.font = FONT
image_FG_draw.fontmode = "L"

text_size = image_FG_draw.textlength(TEXT)
render_offset = -16                         # set offset of the start
render_x_pos = 0 + render_offset            # set start x pos
render_y_pos = RESOLUTION[1] - 128          # set y pos

total_words = round((RESOLUTION[0] / (text_size + 4))) + 1
accent_word = total_words - 3               # set which word will be highlighted as a full solid color
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

while current_word < total_words:
    col = transp_col
    if current_word == accent_word:
        col = accent_col
    image_FG_draw.text((render_x_pos, render_y_pos), TEXT, fill=col)

    render_x_pos += text_size + 4
    current_word += 1

image.paste(image_FG)
image = Image.alpha_composite(image_BG, image_FG)
image.show()
image.save("./image.png")
