# Install Poetry

See our [Initial Configuration](INITIAL_CONFIG.md) for instructions on installing `python` and `poetry`.

# Create Your Plugin

## Creating the Plugin Project

Navigate to the directory where you want to create your plugin and run:

```bash
mkdir copilot-plugin-example
cd copilot-plugin-example
# In plugin directory
poetry init
# Setup versions etc. from INITIAL_CONFIG.md
poetry add django
poetry shell
django-admin start copilot_plugin_example
#mv copilot_plugin_example/* .
```

## Installing the Plugin in Capital Copilot -- Local Development

To install (locally) to an instance of Capital Copilot, you can use the following command:

- the `-e` flag is used to install the plugin in "editable" mode, which means that changes to the plugin will be
  reflected in the Capital Copilot project without needing to reinstall the plugin
- the path to the plugin is relative to the Capital Copilot project directory

```bash
# In Capital Copilot project directory
$ poetry add ../copilot-plugin-example -e

Updating dependencies
Resolving dependencies... (0.2s)

Package operations: 1 install, 0 updates, 0 removals

  • Installing copilot-plugin-example (0.1.0 /Users/user/projects/copilot-plugin-example)

Writing lock file
```

If your plugin is only for development, you can use the following command:

- the `--group dev` flag is used to add the plugin to the `dev-dependencies` section of the `pyproject.toml` file

```bash
poetry add ../copilot-plugin-example --group dev -e
```

## Installing the Plugin in Capital Copilot -- Remote Production Dependency

Then run:

```bash
poetry add copilot-plugin-example
```
