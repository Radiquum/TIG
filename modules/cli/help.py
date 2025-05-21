import sys
from rich import print


def print_main_help(program_name: str):
    print(f"Usage: {program_name} [-h] [-c config_path] <config,draw>")
    print(f"")
    print(f"commands:")
    print(f"config              modify config file")
    print(f"draw                generate an image from provided text")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)


def print_config_cmd_help(program_name: str):
    print(f"Usage: {program_name} [-c config_path] config [-h] <set,inspect>")
    print(f"")
    print(f"commands:")
    print(f"set                 set configuration")
    print(f"inspect             display configuration")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)


def print_config_set_cmd_help(program_name: str):
    print(
        f"Usage: {program_name} [-c config_path] config set [-h] <section>.<key> <value>"
    )
    print(f"")
    print(f"arguments:")
    print(f"section.key         section.key inside of config, one of:")
    print(f"                        resolution:")
    print(f"                            - width")
    print(f"                            - height")
    print(f"                        font:")
    print(f"                            - file")
    print(f"                            - size")
    print(f"                        text:")
    print(f"                            - color")
    print(f"                        background:")
    print(f"                            - color")
    print(f"value               value to set")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)


def print_config_inspect_cmd_help(program_name: str):
    print(f"Usage: {program_name} [-c config_path] config inspect [-h] <yaml,json>")
    print(f"")
    print(f"arguments:")
    print(f"yaml                display configuration in yaml format")
    print(f"json                display configuration in json format")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)


def print_draw_cmd_help(program_name: str):
    print(f"Usage: {program_name} [-c config_path] draw [-h] <line,fill>")
    print(f"")
    print(f"commands:")
    print(f"line                draw a line of repeated text")
    print(f"fill                draw multiple lines of repeated text that fill the image")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)


def print_draw_cmd_cmd_help(program_name: str, cmd: str):
    print(f"Usage: {program_name} [-c config_path] draw {cmd} [-h] <text> [--opacity] [--accent] [--resolution] [--margin]")
    print(f"                                                  [--x-offset] [--x-pos] [--y-offset] [--y-pos]")
    print(f"                                                  [--text-color] [--background-color] [--font-size]")
    print(f"                                                  [--calc] [--preview]")
    print(f"")
    print(f"arguments:")
    print(f"text                  define what text to draw")
    print(f"")
    print(f"options:")
    print(f"-h, --help            show this help message and exit")
    print(f"-c, --config          path to a config file, default: config.yaml")
    print(f"--opacity   0-1       how transparent not accented words or lines will be")
    print(f"--accent    number    what word or line will should be accented")
    print(f"--resolution WxH      overwrite resolution")
    print(f"--margin              set margin between words")
    print(f"--x-pos               set start x position")
    print(f"--x-offset            offset the x position")
    print(f"--y-pos               set start y position")
    print(f"--y-offset            offset the y position")
    print(f"--text-color xxxxxx   overwrite text color")
    print(f"--background-color    overwrite background color")
    print(f"--font-size           overwrite font size")
    print(f"--calc                calculate how much words or lines will be on image")
    print(f"--preview             open and don't save the image after generating")
    sys.exit(0)

