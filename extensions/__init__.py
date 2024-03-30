import importlib
import os


def load_plugins(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # strip '.py' to get module name
            import_path = f"extensions.plugins.{module_name}"
            importlib.import_module(import_path)


plugins_directory = os.path.join(os.path.dirname(__file__), "plugins")
load_plugins(plugins_directory)
