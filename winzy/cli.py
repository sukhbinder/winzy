from .plugins import pm, get_plugins, load_plugins, install_plugin
import argparse
import os


def show_help(args):
    print("winzy update")


def add_alias(args):
    """Add a command alias by creating a batch file in ~/.local/bin/"""
    # Parse the alias command
    if "=" not in args.alias_cmd:
        print("Invalid alias format. Use format: alias=command")
        return

    alias_name, command = args.alias_cmd.split("=", 1)
    alias_name = alias_name.strip()
    command = command.strip()

    if not alias_name or not command:
        print("Invalid alias format. Both alias name and command are required.")
        return

    # Get user's home directory
    home_dir = os.path.expanduser("~")
    local_bin_dir = os.path.join(home_dir, ".local", "bin")

    # Create the .local/bin directory if it doesn't exist
    os.makedirs(local_bin_dir, exist_ok=True)

    # Path for the batch file
    batch_file_path = os.path.join(local_bin_dir, f"{alias_name}.bat")

    # Check if the batch file already exists
    if os.path.exists(batch_file_path):
        response = input(f"Alias '{alias_name}' already exists. Overwrite? (y/N): ")
        if response.lower() not in ["y", "yes"]:
            print("Operation cancelled.")
            return

    # Create the batch file content
    batch_content = f"@echo off\n{command}\n"

    # Write the batch file
    with open(batch_file_path, "w") as f:
        f.write(batch_content)

    print(f"Alias '{alias_name}' created successfully!")
    print(f"Batch file created at: {batch_file_path}")
    print("Make sure ~/.local/bin is in your PATH to use the alias.")


class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action(self, action):
        if isinstance(action, argparse._SubParsersAction):
            return (
                "\n".join(
                    f" {name:<20} {sub.description}"
                    for name, sub in action.choices.items()
                )
                + "\n"
            )
        return super()._format_action(action)


def install_cmd(args):
    install_plugin(
        args.packages,
        args.upgrade,
        args.editable,
        args.force_reinstall,
        args.no_cache_dir,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Win Utils for common tasks in windows",
        formatter_class=CustomHelpFormatter,
    )
    parser.set_defaults(func=show_help)

    subparser = parser.add_subparsers(dest="command")

    # add plugins command
    pugs_p = subparser.add_parser("plugins", description="Get all listed plugins")
    pugs_p.set_defaults(func=get_plugins)

    install_parser = subparser.add_parser(
        "install", description="Install plugins in the same environemnt as winzy"
    )
    install_parser.add_argument("--upgrade", action="store_true")
    install_parser.add_argument("--editable", help="Edit mode for packages")
    install_parser.add_argument("--force-reinstall", action="store_true")
    install_parser.add_argument("--no-cache-dir", action="store_true")
    install_parser.add_argument("packages", nargs="+")
    install_parser.set_defaults(func=install_cmd)

    # add add-alias command
    alias_parser = subparser.add_parser(
        "add-alias", description="Create a command alias by generating a batch file"
    )
    alias_parser.add_argument(
        "alias_cmd", help="Alias command in format 'alias=command', e.g., 'ls=dir $*'"
    )
    alias_parser.set_defaults(func=add_alias)

    pm.hook.register_commands(subparser=subparser)
    load_plugins()
    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
