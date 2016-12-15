import logging

from thrift.transport.TTransport import TMemoryBuffer
from threading import Lock

from frugal.context import _OPID_HEADER
from frugal.exceptions import FException
from frugal.exceptions import FContextException
from frugal.util.headers import _Headers

logger = logging.getLogger(__name__)


class FRegistry(object):
    """
    Registry is responsible for multiplexing received
    messages to the appropriate callback.
    """
    def register(self, context, callback):
        """Register a callback for a given FContext.

        Args:
            context: FContext to register.
            callback: function to register.
        """
        pass

    def unregister(self, context):
        """Unregister the callback for a given FContext.

        Args:
            context: FContext to unregister.
        """
        pass

    def execute(self, frame):
        """Dispatch a single Frugal message frame.

        Args:
            frame: an entire Frugal message frame.
        """
        pass


class FRegistryImpl(FRegistry):
    """
    FRegistryImpl is intended for use only by Frugal clients.
    This is only to be used by generated code.
    """

    def __init__(self):
        self._handlers = {}
        self._handlers_lock = Lock()
        self._next_opid = 0
        self._opid_lock = Lock()

    def register(self, context, callback):
        """Register a callback for a given FContext.

        Args:
            context: FContext to register.
            callback: function to register.
        """
        # An FContext can be reused for multiple requests. Because of this,
        # every time an FContext is registered, it must be assigned a new op id
        # to ensure we can properly correlate responses. We use a monotonically
        # increasing atomic uint64 for this purpose. If the FContext already
        # has an op id, it has been used for a request. We check the handlers
        # map to ensure that request is not still in-flight.
        with self._handlers_lock:
            if str(context._get_op_id()) in self._handlers:
                raise FContextException("context already registered")

        op_id = self._increment_and_get_next_op_id()
        context._set_op_id(op_id)

        with self._handlers_lock:
            self._handlers[str(op_id)] = callback

    def unregister(self, context):
        """Unregister the callback for a given FContext.

        Args:
            context: FContext to unregister.
        """
        with self._handlers_lock:
            self._handlers.pop(str(context._get_op_id()), None)

    def execute(self, frame):
        """Dispatch a single Frugal message frame.

        Args:
            frame: an entire Frugal message frame.
        """
        if not frame:
            return
        headers = _Headers.decode_from_frame(frame)
        op_id = headers.get(_OPID_HEADER, None)

        if not op_id:
            raise FException("Frame missing op_id")

        with self._handlers_lock:
            handler = self._handlers.get(op_id, None)
            if not handler:
                return

            handler(TMemoryBuffer(frame))

    def _increment_and_get_next_op_id(self):
        with self._opid_lock:
            self._next_opid += 1
            op_id = self._next_opid
        raise op_id
