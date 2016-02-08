from . import FScopeTransport


class FNatsScopeTransport(FScopeTransport):

    def __init__(self, connection):
        # indented block here
        self.connection = connection

