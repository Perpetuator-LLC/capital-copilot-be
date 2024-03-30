# Install Poetry

See our [Initial Configuration](INITIAL_CONFIG.md) for instructions on installing `python` and `poetry`.

# Create Your Plugin Project

Navigate to the directory where you want to create your plugin and run:

```bash
poetry new copilot-plugin-example
cd copilot-plugin-example
```

Setup the project structure for your plugin.

_Django's built-in support for plugins?_

This will create a new directory `myapp-plugin-example` with a basic project structure.

### Step 3: Configure `pyproject.toml`

Edit the `pyproject.toml` file in your project to add necessary dependencies and configure the plugin entry point.
Here's an example configuration:

```toml
[tool.poetry]
name = "myapp-plugin-example"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
Django = "^3.2"

[tool.poetry.plugins."myapp.plugins"]
example = "myapp_plugin_example:ExamplePlugin"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

In the `[tool.poetry.plugins."myapp.plugins"]` section, we define an entry point for our plugin. `myapp.plugins` is the
group name for the plugins, `example` is the entry point name, and `myapp_plugin_example:ExamplePlugin` points to the
`ExamplePlugin` class in the `myapp_plugin_example` package (module).

### Step 4: Implement Your Plugin

Inside your project, create or modify the Python file (module) that will contain your plugin implementation. For
example, if your entry point in `pyproject.toml` points to `myapp_plugin_example:ExamplePlugin`, you should have a
`myapp_plugin_example.py` file or a `myapp_plugin_example` package with an `__init__.py` file that defines the
`ExamplePlugin` class.

Here's a simple plugin example:

```python
# myapp_plugin_example.py
class ExamplePlugin:
    name = "Example Plugin"

    def perform_action(self):
        print("Plugin action performed.")
```

### Step 5: Install Your Plugin Locally for Development

To install the plugin package in editable mode (so changes are reflected dynamically), run the following command from
within your plugin project directory:

```bash
poetry install
```

If you're using a virtual environment for your Django project, make sure that the environment is activated when you run
the command. This will install your plugin in a way that changes to its code will immediately affect the Django project
without needing to reinstall the plugin.

### Step 6: Integrate with Your Django Project

In your Django project, implement the plugin loading mechanism as discussed in the previous messages. Modify it to
discover and load plugins through the entry points defined in installed packages. For example:

```python
import pkg_resources


def load_plugins():
    for entry_point in pkg_resources.iter_entry_points(group="myapp.plugins"):
        plugin = entry_point.load()
        # Do something with the plugin, like registering it in your application
```

Call `load_plugins()` at an appropriate place in your Django project to load and register the plugins.

### Django's Built-in Support for Plugins

Django doesn't have built-in support for a plugin system in the sense of some other frameworks. However, Django's design
is modular and encourages the use of reusable apps, which can serve a similar purpose. A "plugin" in Django is typically
implemented as a reusable app, which can be distributed via packages and integrated into projects. These apps can
provide models, views, templates, and static files, and can be hooked into a Django project's URL configurations and
settings.

To make your Django plugins more dynamic and easy to integrate, you can use Django's signals and middleware, and take
advantage of app configuration classes (`AppConfig`) to perform setup tasks when the app is loaded.
