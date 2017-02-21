from __future__ import print_function

import logging
import sys

from thrift.protocol.TBinaryProtocol import TBinaryProtocolFactory
from thrift.protocol.TJSONProtocol import TJSONProtocolFactory
from thrift.protocol.TCompactProtocol import TCompactProtocolFactory
from thrift.Thrift import TApplicationException
from frugal.protocol import FProtocolFactory

PREAMBLE_HEADER = "preamble"
RAMBLE_HEADER = "ramble"


def get_nats_options():
    return {
        "verbose": True,
        "servers": ["nats://127.0.0.1:4222"]
        }


def get_protocol_factory(protocol):
    """
    Returns a protocol factory associated with the string protocol passed in
    as a command line argument to the cross runner

    :param protocol: string
    :return: Protocol factory
    """
    if protocol == "binary":
        return FProtocolFactory(TBinaryProtocolFactory())
    elif protocol == "compact":
        return FProtocolFactory(TCompactProtocolFactory())
    elif protocol == "json":
        return FProtocolFactory(TJSONProtocolFactory())
    else:
        logging.error("Unknown protocol type: %s", protocol)
        sys.exit(1)


def check_for_failure(actual, expected):
    """
    Compares the actual return results with the expected results.

    :return: Bool reflecting failure status

    """
    failed = False
    # TApplicationException doesn't implement __eq__ operator
    if isinstance(expected, TApplicationException):
        print('checking TApplicationException')
        try:
            # Py2 and Py3 versions of thrift slightly differ in how the attribute is assigned...
            if sys.version_info[0] == 3 and actual.message.find(expected.message) == -1 or actual.type != expected.type:
                failed = True
            if sys.version_info[0] == 2 and actual._message.find(expected._message) == -1 or actual.type != expected.type:
                failed = True
        except Exception:
            print('failing TApplicationException')
            failed = True
    elif expected != actual:
        print('failing')
        failed = True
    if failed:
        if sys.version_info[0] == 3:
            print('hello')
            print('type expected:', type(expected))
            print('type actual:', type(actual))
            print("Unexpected result, expected:\n{e}\n but received:\n{a} ".format(
                e=expected, a=actual))
            print('hello2')
        if sys.version_info[0] == 2:
            print("Unexpected result, expected:\n{e}\n but received:\n{a} ".format(
                e=string_of_all_the_things(expected), a=string_of_all_the_things(actual)))

    return failed


def string_of_all_the_things(thing):
    print(sys.version_info, sys.version_info[0])
    if sys.version_info[0] == 2 and isinstance(thing, unicode):
        return thing.encode('ascii', 'ignore')
    else:
        try:
            return thing.decode()
        except:
            return thing