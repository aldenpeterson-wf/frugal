
class FScopeProvider(object):
    """
    FScopeProviders produce FScopeTransports and FProtocols for use
    with Frugal Publishers and Subscribers.
    """

    def __init__(self, transport_factory, protocol_factory):
        self._transport_factory = transport_factory
        self._protocol_factory = protocol_factory

    def build_client(self):
        transport = self._transport_factory.get_transport()
        protocol = self._protocol_factory.get_protocol(transport)
        return (transport, protocol)


class FServiceProvider(object):
    """
    FServiceProviders produce FTransports and FProtocolFactories for use with
    Frugal services and clients.
    """

    def __init__(self, transport, protocol_factory):
        self._transport = transport
        self._protocol_factory = protocol_factory

    def get_transport(self):
        return self._transport

    def get_protocol_factory(self):
        return self._protocol_factory
