from shared.config import config
from modules.cli.help import (
    print_config_cmd_help,
    print_config_inspect_cmd_help,
    print_config_set_cmd_help,
    print_main_help,
    print_draw_cmd_help,
    print_draw_cmd_cmd_help,
)
from shared.util import generate_random_symbols, check_int
from rich import print
import os
import sys
from modules.draw.line import draw_line
from modules.draw.fill import draw_fill

if os.path.exists("config.yaml"):
    config.load()

arguments = sys.argv.copy()


def shift_argv():
    global arguments
    if len(arguments) == 0:
        return None

    _arg = arguments[0]
    arguments = arguments[1::]
    return _arg


program_name = shift_argv()
cmd_or_arg = shift_argv()

if not cmd_or_arg or cmd_or_arg in ["help", "-h", "--help"]:
    print_main_help(program_name)

if cmd_or_arg in ["-c", "--config"]:
    path: str = shift_argv()
    if not path:
        print(f"[bold red]ERROR:[/bold red] path to config is not provided")
        sys.exit(1)
    if not path.endswith(".yaml"):
        print(f"[bold red]ERROR:[/bold red] File not in `.yaml` format")
        sys.exit(1)
    config.load(path)
    cmd_or_arg = shift_argv()
    if not cmd_or_arg:
        print_main_help(program_name)

if cmd_or_arg == "config":
    cmd_or_arg = shift_argv()
    if not cmd_or_arg or cmd_or_arg in ["help", "-h", "--help"]:
        print_config_cmd_help(program_name)
    if cmd_or_arg == "inspect":
        cmd_or_arg = shift_argv()
        if not cmd_or_arg or cmd_or_arg in ["help", "-h", "--help"]:
            print_config_inspect_cmd_help(program_name)
        if cmd_or_arg == "yaml":
            print(config.yaml())
            sys.exit(0)
        if cmd_or_arg == "json":
            print(config.dict())
            sys.exit(0)
    if cmd_or_arg == "set":
        cmd_or_arg = shift_argv()
        if not cmd_or_arg or cmd_or_arg in ["help", "-h", "--help"]:
            print_config_set_cmd_help(program_name)

        sk = cmd_or_arg.split(".")
        if len(sk) < 2 or sk[1] == "":
            print(
                f"[bold red]ERROR:[/bold red] expected: section.key, got: {cmd_or_arg}"
            )
            print_config_set_cmd_help(program_name)

        if sk[0] not in config.get_keys():
            print(
                f"[bold red]ERROR:[/bold red] wrong section name: {sk[0]}, should be one of {", ".join(config.get_keys())}"
            )
            print_config_set_cmd_help(program_name)

        if sk[0] == "resolution":
            if sk[1] not in config.get_section_keys("resolution"):
                print(
                    f"[bold red]ERROR:[/bold red] wrong section key: {sk[1]}, should be one of {", ".join(config.get_section_keys("resolution"))}"
                )
                print_config_set_cmd_help(program_name)
        if sk[0] == "font":
            if sk[1] not in config.get_section_keys("font"):
                print(
                    f"[bold red]ERROR:[/bold red] wrong section key: {sk[1]}, should be one of {", ".join(config.get_section_keys("font"))}"
                )
                print_config_set_cmd_help(program_name)
        if sk[0] in ["text", "background"]:
            if sk[1] not in config.get_section_keys("text"):
                print(
                    f"[bold red]ERROR:[/bold red] wrong section key: {sk[1]}, should be one of {", ".join(config.get_section_keys("text"))}"
                )
                print_config_set_cmd_help(program_name)

        cmd_or_arg = shift_argv()
        if not cmd_or_arg:
            print(f"[bold red]ERROR:[/bold red] value not provided")
            print_config_set_cmd_help(program_name)

        chk, exp_type = config.check_value_type(sk[0], sk[1], cmd_or_arg)
        if chk is not True:
            print(f"[bold red]ERROR:[/bold red] value should be a {exp_type}")
            sys.exit(1)
        if exp_type == "number":
            cmd_or_arg = int(cmd_or_arg)
        if exp_type == "xxxxxx":
            cmd_or_arg = f"#{cmd_or_arg}"

        config.update_and_save(sk[0], sk[1], cmd_or_arg)
        sys.exit(0)

if cmd_or_arg == "draw":
    cmd = shift_argv()
    if not cmd or cmd in ["help", "-h", "--help"]:
        print_draw_cmd_help(program_name)

    arg = shift_argv()
    if arg in ["help", "-h", "--help", None]:
        print_draw_cmd_cmd_help(program_name, cmd)

    text = arg
    arg = shift_argv()

    opacity = 0.25
    if arg == "--opacity":
        opacity = shift_argv()
        if not opacity:
            print(f"[bold red]ERROR:[/bold red] opacity value not provided")
            sys.exit(1)
        opacity = float(opacity)
        arg = shift_argv()

    accent = -3
    gradient_step = 0.1
    if cmd == "fill" and "--angle" in arguments:
        gradient_step = 0.01
    if arg == "--accent":
        accent = shift_argv()
        if not accent:
            print(f"[bold red]ERROR:[/bold red] accent value not provided, should be a number, 'off', 'all' or 'gradient'")
            sys.exit(1)
        if check_int(accent):
            accent = int(accent)
        else:
            if accent not in ["off", "all", "gradient"]:
                print(f"[bold red]ERROR:[/bold red] invalid accent value not provided, should be a number, 'off', 'all' or 'gradient'")
                sys.exit(1)
        arg = shift_argv()
        if accent == "gradient" and not arg.startswith("--"):
            gradient_step = float(arg)
            arg = shift_argv()

    width = config.get_section_key("resolution", "width")
    height = config.get_section_key("resolution", "height")
    if arg == "--resolution":
        resolution = shift_argv()
        if not resolution:
            print(f"[bold red]ERROR:[/bold red] resolution value not provided")
            sys.exit(1)

        resolution = resolution.split("x")
        if len(resolution) < 2 or resolution[1] == "":
            print(
                f"[bold red]ERROR:[/bold red] invalid resolution value provided, should be WxH"
            )
            sys.exit(1)

        width = int(resolution[0])
        height = int(resolution[1])
        arg = shift_argv()

    x_margin = 4
    if arg == "--x-margin":
        x_margin = shift_argv()
        if not x_margin:
            print(f"[bold red]ERROR:[/bold red] x margin value not provided")
            sys.exit(1)
        x_margin = int(x_margin)
        arg = shift_argv()

    y_margin = -24
    if arg == "--x-margin":
        y_margin = shift_argv()
        if not y_margin:
            print(f"[bold red]ERROR:[/bold red] y margin value not provided")
            sys.exit(1)
        y_margin = int(y_margin)
        arg = shift_argv()

    x_offset = 0
    if arg == "--x-offset":
        x_offset = shift_argv()
        if not x_offset:
            print(f"[bold red]ERROR:[/bold red] x offset value not provided")
            sys.exit(1)
        x_offset = int(x_offset)
        arg = shift_argv()

    x_pos = 0
    if arg == "--x-pos":
        x_pos = shift_argv()
        if not x_pos:
            print(f"[bold red]ERROR:[/bold red] x pos value not provided")
            sys.exit(1)
        x_pos = int(x_pos)
        arg = shift_argv()

    y_offset = 0
    if arg == "--y-offset":
        y_offset = shift_argv()
        if not y_offset:
            print(f"[bold red]ERROR:[/bold red] y offset value not provided")
            sys.exit(1)
        y_offset = int(y_offset)
        arg = shift_argv()

    y_pos = 0
    if arg == "--y-pos":
        y_pos = shift_argv()
        if not y_pos:
            print(f"[bold red]ERROR:[/bold red] y pos value not provided")
            sys.exit(1)
        y_pos = int(y_pos)
        arg = shift_argv()

    text_color = config.get_section_key("text", "color")
    if arg == "--text-color":
        text_color = shift_argv()
        if not text_color:
            print(f"[bold red]ERROR:[/bold red] text color value not provided")
            sys.exit(1)
        text_color = f"#{text_color}"
        arg = shift_argv()

    bg_color = config.get_section_key("background", "color")
    if arg == "--background-color":
        bg_color = shift_argv()
        if not bg_color:
            print(f"[bold red]ERROR:[/bold red] background color value not provided")
            sys.exit(1)
        bg_color = f"#{bg_color}"
        arg = shift_argv()

    font_file = config.get_section_key("font", "file")
    font_size = config.get_section_key("font", "size")
    if arg == "--font-size":
        font_size = shift_argv()
        if not font_size:
            print(f"[bold red]ERROR:[/bold red] font size value not provided")
            sys.exit(1)
        font_size = int(font_size)
        arg = shift_argv()

    angle = 0
    if arg == "--angle":
        angle = shift_argv()
        if not angle:
            print(f"[bold red]ERROR:[/bold red] angle value not provided")
            sys.exit(1)
        angle = int(angle)
        arg = shift_argv()

    angle_x_pos = 0
    if arg == "--angle-x-pos":
        angle_x_pos = shift_argv()
        if not angle_x_pos:
            print(f"[bold red]ERROR:[/bold red] angle x pos value not provided")
            sys.exit(1)
        angle_x_pos = int(angle_x_pos)
        arg = shift_argv()

    angle_y_pos = 0
    if arg == "--angle-y-pos":
        angle_y_pos = shift_argv()
        if not angle_y_pos:
            print(f"[bold red]ERROR:[/bold red] angle y pos value not provided")
            sys.exit(1)
        angle_y_pos = int(angle_y_pos)
        arg = shift_argv()

    preview_only = False
    if arg == "--preview":
        preview_only = True
        arg = shift_argv()

    if len(arguments) > 0:
        print(f"[bold red]ERROR:[/bold red] some arguments weren't processed")
        print(f"{arguments}")
        sys.exit(1)

    print(f"[bold green]------ USING PARAMS ------[/bold green]")
    print(f"mode:       {cmd}")
    print(f"resolution: {width}x{height}px")
    print(f"font:       {font_file}, {font_size}pt")
    print(f"colors:     FG: {text_color}, BG: {bg_color}")
    print(f"            opacity:  {opacity}")
    print(f"accent:     {accent}  ")
    print(f"margin:     hor: {x_margin}, ver: {y_margin}")
    print(f"x:          pos: {x_pos}, offset: {x_offset}")
    print(f"y:          pos: {y_pos}, offset: {y_offset}")
    print(f"angle:      {angle}, x: {angle_x_pos}, y: {angle_y_pos}")
    print(f"[bold green]--------------------------[/bold green]")

    if cmd == "line":
        image = draw_line(
            width,
            height,
            font_file,
            font_size,
            text,
            text_color,
            bg_color,
            x_offset,
            x_pos,
            y_offset,
            y_pos,
            opacity,
            accent,
            x_margin,
            angle,
            angle_x_pos,
            angle_y_pos,
            gradient_step
        )

    if cmd == "fill":
        image = draw_fill(
            width,
            height,
            font_file,
            font_size,
            text,
            text_color,
            bg_color,
            x_offset,
            x_pos,
            y_offset,
            y_pos,
            opacity,
            accent,
            x_margin,
            y_margin,
            angle,
            gradient_step
        )

    image.show()
    if not preview_only:
        image.save(
            f"{cmd}_{width}x{height}_fg-{text_color[1:]}_bg-{bg_color[1:]}_{generate_random_symbols(6)}.png"
        )

    sys.exit(0)
