import logging
from . import FServer

logger = logging.getLogger(__name__)


class FNatsServer(FServer):

    def __init__(self):
        logger.exception()

    def serve(self):
        # self.connection.QueueSubscribe(self.subject, queue, callback)


