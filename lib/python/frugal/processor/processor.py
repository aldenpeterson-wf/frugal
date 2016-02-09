
class FProcessor(object):

    def process(in_protocol, out_protocol):
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
