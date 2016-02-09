from thrift import TProtocolFactory
from . import FProtocol


class FProtocolFactory(TProtocolFactory):

    def __init__(self, t_protocol_factory):
        self._t_protocol_factory = t_protocol_factory

    def get_protocol(self, transport):
        return FProtocol(self._t_protocol_factory.getProtocol(transport))
