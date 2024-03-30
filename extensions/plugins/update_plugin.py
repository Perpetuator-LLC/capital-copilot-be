import logging

from extensions.plugin_base import ActionProvider
from extensions.views import task_detail


class Update(ActionProvider):
    title = "update"
    view = task_detail
    # def perform(self):
    #     logging.info("Updating a record")
