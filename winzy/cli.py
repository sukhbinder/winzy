
from .plugins import pm, get_plugins, load_plugins, install_plugin
import argparse


def show_help(args):
    print("winzy update")


class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action(self, action):
        if isinstance(action, argparse._SubParsersAction):
            return "\n".join(f" {name:<20} {sub.description}" for name, sub in action.choices.items()) + "\n"
        return super()._format_action(action)


def install_cmd(args):
    install_plugin(args.packages, args.upgrade, args.editable, args.force_reinstall, args.no_cache_dir)

def main():
    parser = argparse.ArgumentParser(description="Win Utils for common tasks in windows",
                                     formatter_class=CustomHelpFormatter)
    parser.set_defaults(func=show_help)
    
    subparser = parser.add_subparsers(dest="command")
    
    # add plugins command
    pugs_p = subparser.add_parser("plugins", description="Get all listed plugins")
    pugs_p.set_defaults(func=get_plugins)

    install_parser = subparser.add_parser('install', description="Install plugins in the same environemnt as winzy")
    install_parser.add_argument('--upgrade', action='store_true')
    install_parser.add_argument('--editable', help='Edit mode for packages')
    install_parser.add_argument('--force-reinstall', action='store_true')
    install_parser.add_argument('--no-cache-dir', action='store_true')
    install_parser.add_argument('packages', nargs='+')
    install_parser.set_defaults(func=install_cmd)


    load_plugins()
    

    pm.hook.register_commands(subparser=subparser)
    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
