#
# Autogenerated by Frugal Compiler (2.0.0-RC5)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#



from datetime import timedelta
from threading import Lock

from gevent.event import AsyncResult
from gevent import Timeout

from frugal.exceptions import FApplicationException
from frugal.exceptions import FMessageSizeException
from frugal.exceptions import FRateLimitException
from frugal.exceptions import FTimeoutException
from frugal.middleware import Method
from frugal.processor import FBaseProcessor
from frugal.processor import FProcessorFunction
from frugal.transport import TMemoryOutputBuffer
from thrift.Thrift import TApplicationException
from thrift.Thrift import TMessageType
from .ttypes import *


class Iface(object):

    def basePing(self, ctx):
        """
        Args:
            ctx: FContext
        """
        pass


class Client(Iface):

    def __init__(self, transport, protocol_factory, middleware=None):
        """
        Create a new Client with a transport and protocol factory.

        Args:
            transport: FTransport
            protocol_factory: FProtocolFactory
            middleware: ServiceMiddleware or list of ServiceMiddleware
        """
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]
        self._transport = transport
        self._protocol_factory = protocol_factory
        self._oprot = protocol_factory.get_protocol(transport)
        self._write_lock = Lock()
        self._methods = {
            'basePing': Method(self._basePing, middleware),
        }

    def basePing(self, ctx):
        """
        Args:
            ctx: FContext
        """
        return self._methods['basePing']([ctx])

    def _basePing(self, ctx):
        event = AsyncResult()
        self._transport.register(ctx, self._recv_basePing(ctx, event))
        try:
            self._send_basePing(ctx)
            result = event.get(timeout=ctx.timeout/1000)
        except Timeout:
            raise FTimeoutException('basePing timed out after {} milliseconds'.format(ctx.timeout))
        finally:
            self._transport.unregister(ctx)
        return result

    def _send_basePing(self, ctx):
        buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('basePing', TMessageType.CALL, 0)
        args = basePing_args()
        args.write(oprot)
        oprot.writeMessageEnd()
        self._transport.send(buffer.getvalue())

    def _recv_basePing(self, ctx, event):
        def basePing_callback(transport):
            iprot = self._protocol_factory.get_protocol(transport)
            iprot.read_response_headers(ctx)
            _, mtype, _ = iprot.readMessageBegin()
            if mtype == TMessageType.EXCEPTION:
                x = TApplicationException()
                x.read(iprot)
                iprot.readMessageEnd()
                if x.type == FApplicationException.RESPONSE_TOO_LARGE:
                    event.set(FMessageSizeException.response(x.message))
                    return
                if x.type == FApplicationException.RATE_LIMIT_EXCEEDED:
                    event.set(FRateLimitException.response(x.message))
                    return
                event.set(x)
                return
            result = basePing_result()
            result.read(iprot)
            iprot.readMessageEnd()
            event.set(None)
        return basePing_callback


class Processor(FBaseProcessor):

    def __init__(self, handler, middleware=None):
        """
        Create a new Processor.

        Args:
            handler: Iface
        """
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]

        super(Processor, self).__init__()
        self.add_to_processor_map('basePing', _basePing(Method(handler.basePing, middleware), self.get_write_lock()))


class _basePing(FProcessorFunction):

    def __init__(self, handler, lock):
        self._handler = handler
        self._lock = lock

    def process(self, ctx, iprot, oprot):
        args = basePing_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = basePing_result()
        try:
            self._handler([ctx])
        except FRateLimitException as ex:
            with self._lock:
                _write_application_exception(ctx, oprot, FApplicationException.RATE_LIMIT_EXCEEDED, "basePing", ex.message)
                return
        except Exception as e:
            with self._lock:
                e = _write_application_exception(ctx, oprot, TApplicationException.UNKNOWN, "basePing", e.message)
            raise e
        with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('basePing', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except FMessageSizeException as e:
                raise _write_application_exception(ctx, oprot, FApplicationException.RESPONSE_TOO_LARGE, "basePing", e.message)


def _write_application_exception(ctx, oprot, typ, method, message):
    x = TApplicationException(type=typ, message=message)
    oprot.write_response_headers(ctx)
    oprot.writeMessageBegin(method, TMessageType.EXCEPTION, 0)
    x.write(oprot)
    oprot.writeMessageEnd()
    oprot.get_transport().flush()
    return x

class basePing_args(object):
    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('basePing_args')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class basePing_result(object):
    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('basePing_result')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

