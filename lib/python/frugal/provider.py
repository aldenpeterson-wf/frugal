
class FScopeProvider(object):

    def __init__(self, scope_transport_factory, protocol_factory):
        self.transport = scope_transport_factory.get_transport()
        self.protocol = protocol_factory.get_protocol(self.transport)

