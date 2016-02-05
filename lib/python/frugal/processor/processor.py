
class FProcessor(object):

    def process(in_protocol, out_protocol):
        pass


class FBaseProcessor(FProcessor):

    def __init__(self, processor_function__map):
        self.processor_function_map = processor_function_map

    def process(in_protocol, out_protocol):
        context = in_protocol.read_request_header()
        message = in_protocol.read_message_begin()

