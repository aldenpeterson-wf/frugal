
class FProcessor(object):
    """
    FProcessor is a generic object which operates upon an
    input stream and writes to some output stream.
    """

    def process(self, iprot, oprot):
        pass


class FBaseProcessor(FProcessor):

    def __init__(self, processor_function_map):
        self.processor_function_map = processor_function_map

    def process(self, iprot, oprot):
        context = iprot.read_request_header()
        message = iprot.read_message_begin()
        processor = self.processor_function_map[message.name]
        if (processor is not None):
            processor.process(context, iprot, oprot)
            return
