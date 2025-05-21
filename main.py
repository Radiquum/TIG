from shared.config import config
from modules.cli.help import (
    print_config_cmd_help,
    print_config_inspect_cmd_help,
    print_config_set_cmd_help,
    print_main_help,
    print_draw_cmd_help,
    print_draw_cmd_cmd_help
)
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
    if cmd == "line" and arg in ["help", "-h", "--help", None]:
        print_draw_cmd_cmd_help(program_name, cmd)

    if cmd == "fill" and arg in ["help", "-h", "--help", None]:
        print_draw_cmd_cmd_help(program_name, cmd)

    sys.exit(0)

if len(arguments) > 0:
    print(
        f"[bold yellow]WARN:[/bold yellow] Not all arguments has been consumed, rest: {arguments}"
    )
