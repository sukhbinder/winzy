import pluggy
from .hookspecs import winzySpec
import pkg_resources
import sys

pm = pluggy.PluginManager("winzy")
pm.add_hookspecs(winzySpec)

def load_plugins():
    for entry_point in pkg_resources.iter_entry_points("winzy.plugins"):
        plugin=entry_point.load()
        pm.register(plugin)

def load_plugins2():
    if not getattr(sys, "_called_from_test", False):
        # Only load plugins if not running tests
        pm.load_setuptools_entrypoints("winzy.plugins")

def get_plugins(args):
    plugins = []
    plugin_to_distinfo = dict(pm.list_plugin_distinfo())
    for plugin in pm.get_plugins():
        plugin_info = {
            "name": plugin.__name__,
            "hooks": [h.name for h in pm.get_hookcallers(plugin)],
        }
        distinfo = plugin_to_distinfo.get(plugin)
        if distinfo:
            plugin_info["version"] = distinfo.version
            plugin_info["name"] = distinfo.project_name
        plugins.append(plugin_info)

    if plugins:
        print("Installed Plugins:")
        for p in plugins:
            print(p["name"])
    else:
        print("No external plugins in env.")
    return plugins
