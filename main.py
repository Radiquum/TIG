from rich import print
from rich.syntax import Syntax
import argparse
from sys import exit

from shared.config import config
from shared.log import log

# --- Argument Parsers

root_parser = argparse.ArgumentParser(add_help=False)
root_parser.add_argument(
    "-c",
    "--config",
    nargs="?",
    default="config.yaml",
    help="Provide a config file path, default: config.yaml",
)

main_parser = argparse.ArgumentParser("./main.py", parents=[root_parser])
command_subparsers = main_parser.add_subparsers(title="command", dest="command")
config_parser = command_subparsers.add_parser("config", parents=[root_parser], help="modify config file")
config_subparsers = config_parser.add_subparsers(title="action", dest="action")

config_set_parser = config_subparsers.add_parser("set", parents=[root_parser], help="set configuration")


config_inspect_parser = config_subparsers.add_parser("inspect", parents=[root_parser], help="display configuration")
config_inspect_parser.add_argument("type", nargs="?", choices=['yaml', 'json'], default="yaml", help="display type, default: yaml")

# ------------

if __name__ == "__main__":
    args = main_parser.parse_args()
    config.load(args.config)
    # print(f"args: {args}")

    if not args.command:
        main_parser.print_usage()
        exit(1)

    if args.command == "config":
        if not args.action:
            config_parser.print_help()
            exit(1)
        if args.action == "inspect":
            log.info(f"inspecting config as {args.type}")
            print("\n")
            match args.type:
                case 'yaml':
                    syntax = Syntax(config.yaml(), "yaml", theme="github-dark", line_numbers=True)
                case 'json':
                    syntax = Syntax(config.json(), "json", theme="github-dark", line_numbers=True)
            print(syntax)
            exit(0)
