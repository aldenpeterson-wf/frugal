from frugal.exceptions import FException


class FRegistry(object):
    """
    Registry is responsible for multiplexing received
    messages to the appropriate callback.
    """
    def register(context):
        pass

    def unregister(context):
        pass

    def execute(frame):
        pass

    def close():
        pass


class FClientRegistry(FRegistry):

    def __init__(self):
        self._handlers = {}

    def register(self, context, callback):
        op_id = context.get_op_id()

        if (op_id in self._handlers):
            raise FException("context already registered")

        self._handlers[op_id] = callback


class FAsyncCallback(object):

    def on_message(transport):
        pass
