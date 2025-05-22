from rich import print
from rich.syntax import Syntax
import argparse
from sys import exit

from shared.config import config
from shared.log import log
from shared.util import check_int, rgb_to_hex, str_to_hex

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

# ------------

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
                exit(0)

            if sk[0] not in config.get_keys():
                log.error(
                    f"invalid section name, expected: {'|'.join(config.get_keys())}, got: {sk[0]}",
                    extra={"highlighter": None},
                )
                exit(0)

            if sk[1] not in config.get_section_keys(sk[0]):
                log.error(
                    f"invalid section key, expected: {'|'.join(config.get_section_keys(sk[0]))}, got: {sk[1]}",
                    extra={"highlighter": None},
                )
                exit(0)

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
                    exit(0)
                args.value = int(args.value)
            elif value_type == "hex[value] | rgb[0-255,0-255,0-255]":
                if args.value.startswith("hex["):
                    allowed_symbols = [
                        "0",
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "a",
                        "b",
                        "c",
                        "d",
                        "e",
                        "f",
                    ]
                    args.value = args.value.strip("hex[").strip("]").lower()
                    if len(args.value) < 6:
                        log.error(
                            f"invalid hex value, it should be in full format (6 symbols), got {args.value} ({len(args.value)} symbols)",
                            extra={"highlighter": None},
                        )
                        exit(0)
                    for index, char in enumerate(args.value, start=1):
                        if char not in allowed_symbols:
                            log.error(
                                f"unexpected symbol `{char}` at index `{index}`, allowed only 0-9 a-f",
                                extra={"highlighter": None},
                            )
                            exit(0)
                    args.value = str_to_hex(args.value)
                elif args.value.startswith("rgb["):
                    allowed_symbols = [str(i) for i in range(0, 256)]
                    args.value = args.value.strip("rgb[").strip("]").split(",")
                    if len(args.value) < 3:
                        log.error(
                            f"invalid rgb value, it should be [[red]red[/red],[green]green[/green],[blue]blue[/blue]] in range 0-255",
                            extra={"highlighter": None, "markup": True},
                        )
                        exit(0)
                    for index, char in enumerate(args.value, start=1):
                        if char not in allowed_symbols:
                            log.error(
                                f"unexpected symbol `{char}` at index `{index}`, allowed only 0-255",
                                extra={"highlighter": None},
                            )
                            exit(0)
                    args.value = rgb_to_hex(
                        int(args.value[0]), int(args.value[1]), int(args.value[2])
                    )
                else:
                    log.error(
                        f"invalid key value type, expected: {value_type}",
                        extra={"highlighter": None},
                    )
                    exit(0)

            if args.debug:
                log.debug(f"value              : {args.value}")

            config.update_and_save(sk[0], sk[1], args.value)
            log.info(f"value of '{sk[0]}.{sk[1]}' updated to '{args.value}'")
            exit(0)
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
            exit(0)
