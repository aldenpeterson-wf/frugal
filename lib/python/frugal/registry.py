from frugal.exceptions import FException


class FRegistry(object):
    """
    Registry is responsible for multiplexing received
    messages to the appropriate callback.
    """
    def register(self, context):
        pass

    def unregister(self, context):
        pass

    def execute(self, frame):
        pass

    def close(self):
        pass


class FServerRegistry(FRegistry):
    """
    FServerRegistry is intended for use only by Frugal servers.
    This is only to be used by generated code.
    """

    def __init__(self, processor, inputProtocolFactory, outputProtocol):
        self._processor = processor
        self._inputProtocolFactory = inputProtocolFactory
        self._outputProtocol = outputProtocol

    def register(self, context, callback):
        pass

    def unregister(self, context):
        pass

    def execute(self, frame):
        self._processor.process(
            #TODO add the TMemoryProtocol
            self._inputProtocolFactory.get_protocol(),
            self._outputProtocol
        )

    def close(self):
        pass


class FClientRegistry(FRegistry):
    """
    FClientRegistry is intended for use only by Frugal clients.
    This is only to be used by generated code.
    """

    def __init__(self):
        self._handlers = {}

    def register(self, context, callback):
        op_id = context.get_op_id()

        if (op_id in self._handlers):
            raise FException("context already registered")

        self._handlers[op_id] = callback

    def unregister(self, context):
        self._handlers.pop(context.get_op_id(), None)

    def execute(self, frame):
        pass

    def close(self):
        pass


class FAsyncCallback(object):

    def on_message(transport):
        pass
