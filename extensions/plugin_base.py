from django.urls import reverse


class PluginMount(type):
    ignore_cls = ["ActionProvider"]

    def __init__(metacls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if not hasattr(metacls, "plugins"):
            metacls.plugins = []
        if name not in PluginMount.ignore_cls:
            metacls.plugins.append(metacls)

    # def get_plugins(metacls, *args, **kwargs):
    #     return [p(*args, **kwargs) for p in metacls.plugins]


class ActionProvider(metaclass=PluginMount):
    """
    Mount point for plugins which refer to actions that can be performed.
    Plugins implementing this reference should provide the following attributes:
    ========  ========================================================
    title     The text to be displayed, describing the action
    url       The URL to the view where the action will be carried out
    selected  Boolean indicating whether the action is the one
              currently being performed
    ========  ========================================================
    """

    def __init__(self, request, *args, **kwargs):
        pass
        # self.url = reverse(self.view, args=args, kwargs=kwargs)
        # self.selected = request.META['PATH_INFO'] == self.url


# class ActionProvider(metaclass=PluginMount):
#     def perform(self):
#         raise NotImplementedError("Subclasses must implement the 'perform' method.")
