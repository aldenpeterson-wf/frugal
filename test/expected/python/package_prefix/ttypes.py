#
# Autogenerated by Frugal Compiler (2.0.6)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import generic_package_prefix.actual_base.python.ttypes
import generic_package_prefix.actual_base.python.constants

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol


class new_thing(object):
    """
    Attributes:
     - wrapped_thing
    """
    def __init__(self, wrapped_thing=None):
        self.wrapped_thing = wrapped_thing

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.wrapped_thing = generic_package_prefix.actual_base.python.ttypes.thing()
                    self.wrapped_thing.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('new_thing')
        if self.wrapped_thing is not None:
            oprot.writeFieldBegin('wrapped_thing', TType.STRUCT, 1)
            self.wrapped_thing.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(self.wrapped_thing)
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

