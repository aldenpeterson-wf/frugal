
import logging
from thrift.protocol import TBinaryProtocol, TCompactProtocol, TJSONProtocol

def get_nats_options():
    return  {
        "verbose": True,
        "servers": ["nats://127.0.0.1:4222"]
    }


def get_protocol_factory(protocol):
    """
    Returns a protocl facotry associated with the string protocol passed in
    as a command line argument to the cross runner

    :param protocol: string
    :return: Protocl factory
    """
    if args.protocol_type == "binary":
        return FProtocolFactory(TBinaryProtocol.TBinaryProtocolFactory())
    elif args.protocol_type == "compact":
        return FProtocolFactory(TCompactProtocol.TCompactProtocolFactory())
    elif args.protocol_type == "json":
        return FProtocolFactory(TJSONProtocol.TJSONProtocolFactory())
    else:
        logging.error("Unknown protocol type: %s", args.protocol_type)
        sys.exit(1)



def check_for_failure(actual, expected):
    if expected != actual:
        print("\nUnexpected result ")
        return True
    return False

