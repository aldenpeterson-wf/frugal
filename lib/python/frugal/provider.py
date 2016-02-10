

class FScopeProvider(object):
    """
    FScopeProviders produce FScopeTransports and FProtocols for use
    with Frugal Publishers and Subscribers.
    """

    def __init__(self, transport_factory, protocol_factory):
        self._transport_factory = transport_factory
        self._protocol_factory = protocol_factory

    def build_client(self):
        t = self._transport_factory.get_transport()
        p = self._protocol_factory.get_protocol(t)
        return Client(t, p)


class Client(object):

    def __init__(self, transport, protocol):
        self._transport = transport
        self._protocol = protocol

    def get_transport(self):
        return self._transport

    def get_protocol(self):
        return self._protocol
