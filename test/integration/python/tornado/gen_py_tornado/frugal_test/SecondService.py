#
# Autogenerated by Thrift Compiler (0.9.3-wk-3)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:tornado
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import logging
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None

from tornado import gen
from tornado import concurrent
from thrift.transport import TTransport

class Iface(object):
  def blahBlah(self):
    pass

  def secondtestString(self, thing):
    """
    Parameters:
     - thing
    """
    pass


class Client(Iface):
  def __init__(self, transport, iprot_factory, oprot_factory=None):
    self._transport = transport
    self._iprot_factory = iprot_factory
    self._oprot_factory = (oprot_factory if oprot_factory is not None
                           else iprot_factory)
    self._seqid = 0
    self._reqs = {}
    self._transport.io_loop.spawn_callback(self._start_receiving)

  @gen.engine
  def _start_receiving(self):
    while True:
      try:
        frame = yield self._transport.readFrame()
      except TTransport.TTransportException as e:
        for future in self._reqs.itervalues():
          future.set_exception(e)
        self._reqs = {}
        return
      tr = TTransport.TMemoryBuffer(frame)
      iprot = self._iprot_factory.getProtocol(tr)
      (fname, mtype, rseqid) = iprot.readMessageBegin()
      future = self._reqs.pop(rseqid, None)
      if not future:
        # future has already been discarded
        continue
      method = getattr(self, 'recv_' + fname)
      try:
        result = method(iprot, mtype, rseqid)
      except Exception as e:
        future.set_exception(e)
      else:
        future.set_result(result)

  def blahBlah(self):
    self._seqid += 1
    future = self._reqs[self._seqid] = concurrent.Future()
    self.send_blahBlah()
    return future

  def send_blahBlah(self):
    oprot = self._oprot_factory.getProtocol(self._transport)
    oprot.writeMessageBegin('blahBlah', TMessageType.CALL, self._seqid)
    args = blahBlah_args()
    args.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def recv_blahBlah(self, iprot, mtype, rseqid):
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      raise x
    result = blahBlah_result()
    result.read(iprot)
    iprot.readMessageEnd()
    return

  def secondtestString(self, thing):
    """
    Parameters:
     - thing
    """
    self._seqid += 1
    future = self._reqs[self._seqid] = concurrent.Future()
    self.send_secondtestString(thing)
    return future

  def send_secondtestString(self, thing):
    oprot = self._oprot_factory.getProtocol(self._transport)
    oprot.writeMessageBegin('secondtestString', TMessageType.CALL, self._seqid)
    args = secondtestString_args()
    args.thing = thing
    args.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def recv_secondtestString(self, iprot, mtype, rseqid):
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      raise x
    result = secondtestString_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "secondtestString failed: unknown result")


class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["blahBlah"] = Processor.process_blahBlah
    self._processMap["secondtestString"] = Processor.process_secondtestString

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
      return
    else:
      return self._processMap[name](self, seqid, iprot, oprot)

  @gen.coroutine
  def process_blahBlah(self, seqid, iprot, oprot):
    args = blahBlah_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = blahBlah_result()
    yield gen.maybe_future(self._handler.blahBlah())
    oprot.writeMessageBegin("blahBlah", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  @gen.coroutine
  def process_secondtestString(self, seqid, iprot, oprot):
    args = secondtestString_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = secondtestString_result()
    result.success = yield gen.maybe_future(self._handler.secondtestString(args.thing))
    oprot.writeMessageBegin("secondtestString", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()


# HELPER FUNCTIONS AND STRUCTURES

class blahBlah_args:

  thrift_spec = (
  )

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
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
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('blahBlah_args')
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class blahBlah_result:

  thrift_spec = (
  )

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
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
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('blahBlah_result')
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class secondtestString_args:
  """
  Attributes:
   - thing
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'thing', None, None, ), # 1
  )

  def __init__(self, thing=None,):
    self.thing = thing

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.thing = iprot.readString()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('secondtestString_args')
    if self.thing is not None:
      oprot.writeFieldBegin('thing', TType.STRING, 1)
      oprot.writeString(self.thing)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.thing)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class secondtestString_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.STRING, 'success', None, None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRING:
          self.success = iprot.readString()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('secondtestString_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRING, 0)
      oprot.writeString(self.success)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.success)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
