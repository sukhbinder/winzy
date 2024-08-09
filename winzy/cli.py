
from .plugins import pm, get_plugins, load_plugins
import argparse


def show_help(args):
    print("winzy update")


def main():
    parser = argparse.ArgumentParser(description="Win Utils for common tasks in windows")
    parser.set_defaults(func=show_help)
    
    subparser = parser.add_subparsers(dest="command")
    
    # add plugins command
    pugs_p = subparser.add_parser("plugins", description="Get all listed plugins")
    pugs_p.set_defaults(func=get_plugins)

    load_plugins()
    

    pm.hook.register_commands(subparser=subparser)
    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
