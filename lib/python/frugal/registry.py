
class Registry(object):
    """
    Registry provides a
    """
    def register(context):
        pass

    def unregister(context):
        pass

    def execute():
        pass

    def close():
        pass


class FServerRegistry(Registry):

    def __init__(self, processor, inputProtocolFactory, outputProtocol):
        self.processor = processor
        self.inputProtocolFactory = inputProtocolFactory
        self.outputProtocol = outputProtocol

    def register(self, context):
        pass

    def unregister(self, context):
        pass

    def execute(self, frame):
        self.processor.process(
            self.inputProtocolFactory.getProtocol(TMemoryInputTransport(frame)),
            self.outputProtocol)

    def close():
        pass
