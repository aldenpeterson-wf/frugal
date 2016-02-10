from thrift.protocol.TProtocol import TProtocolBase


class FProtocol(TProtocolBase):
    """
    FProtocol is an extension of thrift TProtocol with the addition of headers
    """

    def __init__(self, t_protocol):
        self._t_protocol = t_protocol

    def write_request_header(self, context):
        pass

    def read_request_header(self):
        pass

    def write_response_header(self, context):
        pass

    def read_response_header(self):
        pass

    def writeMessageBegin(self, name, ttype, seqid):
        self._t_protocol.writeMessageBegin(self, name, ttype, seqid)

    def writeMessageEnd(self):
        self._t_protocol.writeMessageEnd(self)

    def writeStructBegin(self, name):
        self._t_protocol.writeStructBegin(self, name)
