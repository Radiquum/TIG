from rich import print
from rich.syntax import Syntax
import argparse
from sys import exit

from shared.config import config
from shared.log import log
from shared.util import check_int, check_color, generate_random_symbols
from modules.draw.line import draw_line
from modules.draw.fill import draw_fill
from modules.draw.square import draw_square
from modules.types.custom import opacity_type, accent_type

# --- Argument Parsers

root_parser = argparse.ArgumentParser(add_help=False)
root_parser.add_argument(
    "-c",
    "--config",
    nargs="?",
    default="config.yaml",
    help="Provide a config file path, path should end with .yaml or .json, default: config.yaml",
)
root_parser.add_argument(
    "--debug",
    action="store_true",
    default=False,
    help="Debug the program",
)

main_parser = argparse.ArgumentParser("./main.py", parents=[root_parser])
command_subparsers = main_parser.add_subparsers(title="command", dest="command")

## --- config parser
config_parser = command_subparsers.add_parser(
    "config", parents=[root_parser], help="modify config file"
)
config_subparsers = config_parser.add_subparsers(title="action", dest="action")

config_set_parser = config_subparsers.add_parser(
    "set",
    parents=[root_parser],
    help="set configuration",
    formatter_class=argparse.RawTextHelpFormatter,
)
config_set_parser.add_argument(
    "sk", help=config.get_config_sections_and_keys_types(), metavar="section.key"
)
config_set_parser.add_argument("value")

config_inspect_parser = config_subparsers.add_parser(
    "inspect", parents=[root_parser], help="display configuration"
)
config_inspect_parser.add_argument(
    "type",
    nargs="?",
    choices=["yaml", "json"],
    default="yaml",
    help="display type, default: yaml",
)

## --- draw parser
draw_parser = command_subparsers.add_parser(
    "draw", parents=[root_parser], help="generate an image from provided text"
)
draw_parser.add_argument(
    "mode",
    metavar="MODE",
    choices=["line", "fill", "square"],
    help="mode to use: line|fill",
)
draw_parser.add_argument("text", metavar="TEXT", help="text to draw")
draw_parser.add_argument(
    "--opacity",
    type=opacity_type,
    default=0.25,
    help="how transparent not accented words or lines will be, default: 0.25; allowed 0-1",
)
draw_parser.add_argument(
    "--accent",
    type=accent_type,
    default=-3,
    help="what word or line will should be accented, default: -3; allowed number|off|all|gradient",
)
draw_parser.add_argument(
    "--gradient-step",
    type=opacity_type,
    default=None,
    help="step in range from 0 to 1 if accent set to gradient",
    metavar="STEP",
)
draw_parser.add_argument("--resolution", help="overwrite resolution", metavar="WxH")
draw_parser.add_argument(
    "--text-color",
    help="overwrite text color",
    metavar="hex[value] | rgb[0-255,0-255,0-255]",
)
draw_parser.add_argument(
    "--bg-color",
    help="overwrite background color",
    metavar="hex[value] | rgb[0-255,0-255,0-255]",
)
draw_parser.add_argument(
    "--font-size", type=int, help="overwrite font size", metavar="SIZE"
)
draw_parser.add_argument(
    "--angle", help="rotate the text by an angle, default: 0", default=0, type=int
)
draw_parser.add_argument(
    "--x-pos", help="set start x position, default: 0", default=0, type=int
)
draw_parser.add_argument(
    "--y-pos", help="set start y position, default: 0", default=0, type=int
)
draw_parser.add_argument(
    "--x-offset", help="offset the x position, default: 0", default=0, type=int
)
draw_parser.add_argument(
    "--y-offset", help="offset the y position, default: 0", default=0, type=int
)
draw_parser.add_argument(
    "--x-margin", help="set margin between words, default: 4", default=4, type=int
)
draw_parser.add_argument(
    "--y-margin", help="set margin between lines, default: -20", default=-20, type=int
)
draw_parser.add_argument(
    "--angle-x-pos",
    help="absolute x position of rotated text, default: 0",
    default=0,
    type=int,
    metavar="X_POS",
)
draw_parser.add_argument(
    "--angle-y-pos",
    help="absolute y position of rotated text, default: 0",
    default=0,
    type=int,
    metavar="Y_POS",
)
draw_parser.add_argument(
    "--preview",
    action="store_true",
    default=False,
    help="don't save the image after generating",
)

## ------------

if __name__ == "__main__":
    args = main_parser.parse_args()
    config.load(args.config)

    if args.debug:
        log.debug("DEBUG MODE")
        log.debug("provided arguments:")
        log.debug(args)
        log.debug("loaded config:")
        log.debug(config.dict())
        print("\n")

    if not args.command:
        main_parser.print_usage()
        exit(1)

    if args.command == "config":
        if not args.action:
            config_parser.print_help()
            exit(1)
        if args.action == "set":
            sk = args.sk.split(".")
            if len(sk) < 2 or sk[1] == "":
                log.error(
                    f"expected: section.key, got: {args.sk}",
                    extra={"highlighter": None},
                )
                exit(1)

            if sk[0] not in config.get_keys():
                log.error(
                    f"invalid section name, expected: {'|'.join(config.get_keys())}, got: {sk[0]}",
                    extra={"highlighter": None},
                )
                exit(1)

            if sk[1] not in config.get_section_keys(sk[0]):
                log.error(
                    f"invalid section key, expected: {'|'.join(config.get_section_keys(sk[0]))}, got: {sk[1]}",
                    extra={"highlighter": None},
                )
                exit(1)

            if args.debug:
                log.debug(f"section    : {sk[0]}")
                log.debug(f"key        : {sk[1]}")
                log.debug(
                    f"value type : {config.get_config_section_key_type(sk[0], sk[1])}"
                )

            value_type = config.get_config_section_key_type(sk[0], sk[1])
            if value_type == "number":
                if not check_int(args.value):
                    log.error(
                        f"invalid key value type, expected: {value_type}",
                        extra={"highlighter": None},
                    )
                    exit(1)
                args.value = int(args.value)
            elif value_type == "hex[value] | rgb[0-255,0-255,0-255]":
                args.value = check_color(args.value)

            if args.debug:
                log.debug(f"value              : {args.value}")

            config.update_and_save(sk[0], sk[1], args.value)
            log.info(f"value of '{sk[0]}.{sk[1]}' updated to '{args.value}'")
        if args.action == "inspect":
            log.info(f"inspecting config as {args.type}")
            print("\n")
            match args.type:
                case "yaml":
                    syntax = Syntax(
                        config.yaml(), "yaml", theme="github-dark", line_numbers=True
                    )
                case "json":
                    syntax = Syntax(
                        config.json(), "json", theme="github-dark", line_numbers=True
                    )
            print(syntax)
    if args.command == "draw":

        if args.gradient_step is None:
            args.gradient_step = 0.1
            if args.mode == "fill" and args.angle != 0:
                args.gradient_step = 0.01

        width = config.get_section_key("resolution", "width")
        height = config.get_section_key("resolution", "height")

        if args.resolution:
            resolution = args.resolution.split("x")
            if len(resolution) < 2 or resolution[1] == "":
                log.error(
                    f"expected: WxH, got: {args.resolution}",
                    extra={"highlighter": None},
                )
                exit(1)
            if not check_int(resolution[0]) or not check_int(resolution[1]):
                log.error(
                    f"resolution should be provided as INTxINT",
                    extra={"highlighter": None},
                )
                exit(1)
            width = int(resolution[0])
            height = int(resolution[1])
            if args.debug:
                log.debug(
                    f"overwrote resolution {config.get_section_key('resolution', 'width')}x{config.get_section_key('resolution', 'height')} -> {width}x{height}",
                    extra={"highlighter": None},
                )

        font_file = config.get_section_key("font", "file")
        font_size = config.get_section_key("font", "size")
        if args.font_size:
            font_size = args.font_size

        text_color = config.get_section_key("text", "color")
        bg_color = config.get_section_key("background", "color")
        if args.text_color:
            text_color = check_color(args.text_color)
        if args.bg_color:
            bg_color = check_color(args.bg_color)

        if args.mode == "square":
            if args.x_margin == 4:
                args.x_margin = 0
            if args.y_margin == -20:
                args.y_margin = 0
            if args.accent == -3:
                args.accent = "all"

        print("[bold green]------ USING PARAMS ------[/bold green]")
        print(f"mode:       {args.mode}")
        print(f"resolution: [bold cyan]{width}x{height}[/bold cyan] px")
        print(f"font:       {font_file}, {font_size} pt")
        print(f"colors:     FG: '{text_color}', BG: '{bg_color}'")
        print(f"            opacity:  {args.opacity}")
        if args.accent == "gradient":
            print(f"accent:     {args.accent}, step: {args.gradient_step}")
        else:
            print(f"accent:     {args.accent}")
        print(f"margin:     hor: {args.x_margin}, ver: {args.y_margin}")
        print(f"x:          pos: {args.x_pos}, offset: {args.x_offset}")
        print(f"y:          pos: {args.y_pos}, offset: {args.y_offset}")
        print(
            f"angle:      {args.angle} deg, x: {args.angle_x_pos}, y: {args.angle_y_pos}"
        )
        print("[bold green]--------------------------[/bold green]")

        if args.mode == "line":
            image = draw_line(
                width,
                height,
                font_file,
                font_size,
                args.text,
                text_color,
                bg_color,
                args.x_offset,
                args.x_pos,
                args.y_offset,
                args.y_pos,
                args.opacity,
                args.accent,
                args.x_margin,
                args.angle,
                args.angle_x_pos,
                args.angle_y_pos,
                args.gradient_step,
            )

        if args.mode == "fill":
            image = draw_fill(
                width,
                height,
                font_file,
                font_size,
                args.text,
                text_color,
                bg_color,
                args.x_offset,
                args.x_pos,
                args.y_offset,
                args.y_pos,
                args.opacity,
                args.accent,
                args.x_margin,
                args.y_margin,
                args.angle,
                args.gradient_step,
            )

        if args.mode == "square":
            image = draw_square(
                width,
                height,
                font_file,
                font_size,
                args.text,
                text_color,
                bg_color,
                args.x_pos,
                args.y_pos,
                args.opacity,
                args.accent,
                args.x_margin,
                args.y_margin,
                args.gradient_step,
            )

        image.show()
        if not args.preview:
            filename = f"{args.mode}_{width}x{height}_fg-{text_color[1:]}_bg-{bg_color[1:]}_{generate_random_symbols(6)}.png"
            image.save(filename)
            log.info(f"Image Saved as '{filename}'")
    exit(0)
