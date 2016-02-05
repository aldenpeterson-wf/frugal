from thrift.Thrift import TTransportBase


class Transport(TTransportBase):

    def set_registry(registry):
        pass

    def register(context, callback):
        pass

    def unregister(context):
        pass

    def set_monitor(monitor):
        pass

    def closed():
        pass
