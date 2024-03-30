# Plugins

Capital Copilot employs a plugin system to allow for the easy addition of new features. The plugin system is loosely
based on the simple plugin framework by Marty Alchin. The framework is a simple way to create a plugin system in Python.
The framework is based on the idea of a plugin being a class that is instantiated and registered with the plugin
manager. The plugin manager then calls the plugin's methods when needed.

References:

- http://martyalchin.com/2008/jan/10/simple-plugin-framework/
- https://web.archive.org/web/20220928004258/http://martyalchin.com/2008/jan/10/simple-plugin-framework/
- https://www.djangosnippets.org/snippets/542/

There are 2 types of plugins:

1. Internal Plugins - Plugins that are part of the Capital Copilot codebase.
2. External Plugins - Plugins that are not part of the Capital Copilot codebase.

External Plugins
