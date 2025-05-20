from shared.config import config
from rich import print
import os
import sys

if os.path.exists("config.yaml"):
    config.load()

arguments = sys.argv.copy()


def shift_argv():
    print("------ ARGS SHIFT -------")
    global arguments
    if len(arguments) == 0:
        print(f"Return ARG: None")
        print(f"REST:       {arguments}")
        print("-------------------------")
        return None

    _arg = arguments[0]
    arguments = arguments[1::]
    print(f"Return ARG: {_arg}")
    print(f"REST:       {arguments}")
    print("-------------------------")
    return _arg


def check_int(s):
    if s[0] in ("-", "+"):
        return s[1:].isdigit()
    return s.isdigit()


program_name = shift_argv()


def print_main_help():
    print(f"Usage: {program_name} [-h] [-c config_path] <config>")
    print(f"")
    print(f"commands:")
    print(f"config              modify config file")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)


def print_config_cmd_help():
    print(f"Usage: {program_name} [-c config_path] config [-h] <set,inspect>")
    print(f"")
    print(f"commands:")
    print(f"inspect             display current loaded configuration")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)


def print_config_set_cmd_help():
    print(
        f"Usage: {program_name} [-c config_path] config set [-h] <section>.<key> <value>"
    )
    print(f"")
    print(f"arguments:")
    print(f"section.key         section.key inside of config, one of:")
    print(f"                        resolution:")
    print(f"                            - width")
    print(f"                            - height")
    print(f"value               value to set")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)


def print_config_inspect_cmd_help():
    print(f"Usage: {program_name} [-c config_path] config inspect [-h] <yaml,json>")
    print(f"")
    print(f"arguments:")
    print(f"yaml                display current loaded configuration in yaml format")
    print(f"json                display current loaded configuration in json format")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)


cmd_or_arg = shift_argv()

if not cmd_or_arg or cmd_or_arg in ["help", "-h", "--help"]:
    print_main_help()

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
        print_main_help()

if cmd_or_arg == "config":
    cmd_or_arg = shift_argv()
    if not cmd_or_arg or cmd_or_arg in ["help", "-h", "--help"]:
        print_config_cmd_help()
    if cmd_or_arg == "inspect":
        cmd_or_arg = shift_argv()
        if not cmd_or_arg or cmd_or_arg in ["help", "-h", "--help"]:
            print_config_inspect_cmd_help()
        if cmd_or_arg == "yaml":
            print(config.yaml())
            sys.exit(0)
        if cmd_or_arg == "json":
            print(config.dict())
            sys.exit(0)
    if cmd_or_arg == "set":
        cmd_or_arg = shift_argv()
        if not cmd_or_arg or cmd_or_arg in ["help", "-h", "--help"]:
            print_config_set_cmd_help()

        sk = cmd_or_arg.split(".")
        if len(sk) < 2 or sk[1] == "":
            print(
                f"[bold red]ERROR:[/bold red] expected: section.key, got: {cmd_or_arg}"
            )
            print_config_set_cmd_help()

        sections = ["resolution"]
        if sk[0] not in sections:
            print(
                f"[bold red]ERROR:[/bold red] wrong section name: {sk[0]}, should be one of {", ".join(sections)}"
            )
            print_config_set_cmd_help()

        if sk[0] == "resolution":
            keys = ["width", "height"]
            if sk[1] not in keys:
                print(
                    f"[bold red]ERROR:[/bold red] wrong section key: {sk[1]}, should be one of {", ".join(keys)}"
                )
                print_config_set_cmd_help()

        cmd_or_arg = shift_argv()
        if not cmd_or_arg:
            print(f"[bold red]ERROR:[/bold red] value not provided")
            print_config_set_cmd_help()

        if sk[0] in [sections[0]] and sk[1] in [keys[0], keys[1]]:
            if not check_int(cmd_or_arg):
                print(f"[bold red]ERROR:[/bold red] value should be a number")
                sys.exit(1)
            cmd_or_arg = int(cmd_or_arg)

        config.update_and_save(sk[0], sk[1], cmd_or_arg)
        sys.exit(0)

if len(arguments) > 0:
    print(
        f"[bold yellow]WARN:[/bold yellow] Not all arguments has been consumed, rest: {arguments}"
    )
