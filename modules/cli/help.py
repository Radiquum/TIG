import sys

def print_main_help(program_name: str):
    print(f"Usage: {program_name} [-h] [-c config_path] <config>")
    print(f"")
    print(f"commands:")
    print(f"config              modify config file")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)


def print_config_cmd_help(program_name: str):
    print(f"Usage: {program_name} [-c config_path] config [-h] <set,inspect>")
    print(f"")
    print(f"commands:")
    print(f"inspect             display current loaded configuration")
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
    print(f"yaml                display current loaded configuration in yaml format")
    print(f"json                display current loaded configuration in json format")
    print(f"")
    print(f"options:")
    print(f"-h, --help          show this help message and exit")
    print(f"-c, --config        path to a config file, default: config.yaml")
    sys.exit(0)