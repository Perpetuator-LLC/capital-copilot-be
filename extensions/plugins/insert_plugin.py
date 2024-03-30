import logging

from extensions.plugin_base import ActionProvider
from extensions.views import task_detail


class Insert(ActionProvider):
    title = "insert"
    view = task_detail
    # def perform(self):
    #     logging.info("Inserting a new record")
