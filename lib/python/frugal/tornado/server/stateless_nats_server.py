import logging
import struct

from thrift.Thrift import TException
from thrift.transport.TTransport import TMemoryBuffer
from tornado import gen

from frugal.server import FServer
from frugal.transport import FBoundedMemoryBuffer
from frugal.tornado.transport.nats_scope_transport import MAX_MESSAGE_SIZE

logger = logging.getLogger(__name__)


# TODO: Rename this to FNatsNatsTornadoServer with 2.0
class FStatelessNatsTornadoServer(FServer):
    """An implementation of FServer which uses NATS as the underlying transport.
    Clients must connect with the FNatsTransport"""

    def __init__(self,
                 nats_client,
                 subject,
                 processor,
                 protocol_factory,
                 queue=""):
        """Create a new instance of FStatelessNatsTornadoServer

        Args:
            nats_client: connected instance of nats.io.Client
            subject: subject to listen on
            processor: FProcess
            protocol_factory: FProtocolFactory
        """
        self._nats_client = nats_client
        self._subject = subject
        self._processor = processor
        self._iprot_factory = protocol_factory
        self._oprot_factory = protocol_factory
        self._queue = queue
        self._sub_id = None

    @gen.coroutine
    def serve(self):
        """Subscribe to provided subject and listen on provided queue"""
        self._sub_id = yield self._nats_client.subscribe(
            self._subject,
            self._queue,
            self._on_message_callback
        )

        logger.info("Frugal server running...")

    @gen.coroutine
    def stop(self):
        """Unsubscribe from server subject"""
        logger.debug("Frugal server stopping...")
        yield self._nats_client.unsubscribe(self._sub_id)

    def set_high_watermark(self, high_watermark):
        """Not implemented"""
        pass

    def get_high_watermark(self):
        """Not implemented"""
        return 0

    @gen.coroutine
    def _on_message_callback(self, msg):
        """Process and respond to server request on server subject

        Args:
            msg: request message published to server subject
        """
        reply_to = msg.reply
        if not reply_to:
            logger.warn("Discarding invalid NATS request (no reply)")
            return

        frame_size = struct.unpack('!I', msg.data[:4])[0]
        if frame_size > MAX_MESSAGE_SIZE - 4:
            logger.warning("Invalid frame size, dropping message.")
            return

        # Read and process frame (exclude first 4 bytes which
        # represent frame size).
        iprot = self._iprot_factory.get_protocol(
            TMemoryBuffer(msg.data[4:])
        )
        out_transport = FBoundedMemoryBuffer(MAX_MESSAGE_SIZE - 4)
        oprot = self._oprot_factory.get_protocol(out_transport)

        try:
            self._processor.process(iprot, oprot)
        except TException as ex:
            logger.exception(ex)
            return

        if len(out_transport) == 0:
            return

        data = out_transport.getvalue()
        buff = struct.pack('!I', len(data))

        yield self._nats_client.publish(reply_to, buff + data)
