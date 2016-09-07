import asyncio
import sys
import argparse

sys.path.append('gen_py_asyncio')
sys.path.append('gen_py_asyncio/frugal_test')   # todo: understand why this isn't working without this, shouldn't the package do this?
sys.path.append('..')

from thrift.protocol import TBinaryProtocol, TCompactProtocol, TJSONProtocol
from thrift.transport.TTransport import TTransportException

from frugal.context import FContext
from frugal.protocol import FProtocolFactory
from frugal.provider import FScopeProvider
from frugal.aio.transport import (
    FNatsTransport,
    FNatsScopeTransportFactory,
)

from nats.aio.client import Client as NatsClient

from frugal_test.f_Events_publisher import EventsPublisher
from frugal_test import ttypes, Xception, Insanity, Xception2, Event
from frugal_test.f_Events_subscriber import EventsSubscriber
from frugal_test.f_FrugalTest import Xtruct, Xtruct2, Numberz
from frugal_test.f_FrugalTest import Client as FrugalTestClient


from common.utils import check_for_failure, get_protocol_factory

async def main():

    parser = argparse.ArgumentParser(description="Run a python tornado client")
    parser.add_argument('--port', dest='port', default=9090)
    parser.add_argument('--protocol', dest='protocol_type', default="binary", choices="binary, compact, json")
    parser.add_argument('--transport', dest='transport_type', default="stateless", choices="stateless, stateful, stateless-stateful, http")

    args = parser.parse_args()

    protocol_factory = get_protocol_factory(args.protocol_type)



    nats_client = NatsClient()
    await nats_client.connect(****get_nats_options())

    nats_transport = FNatsTransport(nats_client, args.port)
    try:
        await nats_transport.open()
    except TTransportException as ex:
        root.error(ex)
        return

    client = FrugalTestClient(nats_transport, protocol_factory)
    ctx = FContext("test")


    await test_rpc(client, ctx)




async def test_rpc(client, ctx):
    test_failed = False

    # RPC with no type
    await client.testVoid(ctx)

    # RPC with string
    thing = "thing"
    result = await client.testString(ctx, "thing")
    test_failed = check_for_failure(result, thing) or test_failed

    # RPC with boolean
    boolean = True
    result = await client.testBool(ctx, boolean)
    test_failed = check_for_failure(result, boolean) or test_failed

    # RPC with byte
    byte = 42
    result = await client.testByte(ctx, byte)
    test_failed = check_for_failure(result, byte) or test_failed

    # RPC with i32
    i32 = 4242
    result = await client.testI32(ctx, i32)
    test_failed = check_for_failure(result, i32) or test_failed

    # RPC with i64
    i64 = 424242
    result = await client.testI64(ctx, i64)
    test_failed = check_for_failure(result, i64) or test_failed

    # RPC with double
    double = 42.42
    result = await client.testDouble(ctx, double)
    test_failed = check_for_failure(result, double) or test_failed


    # RPC with binary
    binary = "0b101010"
    result = await client.testBinary(ctx, binary)
    test_failed = check_for_failure(result, binary) or test_failed

    # # RPC with Xtruct
    struct = Xtruct()
    struct.string_thing = thing
    struct.byte_thing = byte
    struct.i32_thing = i32
    struct.i64_thing = i64
    print("testStruct({}) = ".format(struct), end="")
    result = await client.testStruct(ctx, struct)
    test_failed = check_for_failure(result, struct) or test_failed

    # RPC with Xtruct2
    struct2 = Xtruct2()
    struct2.struct_thing = struct
    struct2.byte_thing = 0
    struct2.i32_thing = 0
    result = await client.testNest(ctx, struct2)
    test_failed = check_for_failure(result, struct2) or test_failed

    # RPC with map
    dictionary = {1: 2, 3: 4, 5: 42}
    result = await client.testMap(ctx, dictionary)
    test_failed = check_for_failure(result, dictionary) or test_failed

    # RPC with map of strings
    string_map = {"a": "2", "b": "blah", "some": "thing"}
    result = await client.testStringMap(ctx, string_map)
    test_failed = check_for_failure(result, string_map) or test_failed

    # RPC with set
    set = {1, 2, 2, 42}
    result = await client.testSet(ctx, set)
    test_failed = check_for_failure(result, set) or test_failed

    # RPC with list
    list = [1, 2, 42]
    result = await client.testList(ctx, list)
    test_failed = check_for_failure(result, list) or test_failed

    # RPC with enum
    enum = Numberz.TWO
    result = await client.testEnum(ctx, enum)
    test_failed = check_for_failure(result, enum) or test_failed

    # RPC with typeDef
    type_def = 42
    result = await client.testTypedef(ctx, type_def)
    test_failed = check_for_failure(result, type_def) or test_failed

    # # RPC with map of maps
    d = {4: 4, 3: 3, 2: 2, 1: 1}
    e = {-4: -4, -3: -3, -2: -2, -1: -1}
    mapmap = {-4: e, 4: d}
    result = await client.testMapMap(ctx, 42)
    test_failed = check_for_failure(result, mapmap) or test_failed

    # RPC with Insanity (xtruct of xtructs)
    truck1 = Xtruct("Goodbye4", 4, 4, 4)
    truck2 = Xtruct("Hello2", 2, 2, 2)
    insanity = Insanity()
    insanity.userMap = {Numberz.FIVE: 5, Numberz.EIGHT: 8}
    insanity.xtructs = [truck1, truck2]
    result = await client.testInsanity(ctx, insanity)
    expected_result = {1:
                     {2: Insanity(
                         xtructs=[Xtruct(string_thing='Goodbye4', byte_thing=4, i32_thing=4, i64_thing=4),
                                  Xtruct(string_thing='Hello2', byte_thing=2, i32_thing=2, i64_thing=2)],
                         userMap={8: 8, 5: 5}),
                      3: Insanity(
                         xtructs=[Xtruct(string_thing='Goodbye4', byte_thing=4, i32_thing=4, i64_thing=4),
                                  Xtruct(string_thing='Hello2', byte_thing=2, i32_thing=2, i64_thing=2)],
                         userMap={8: 8, 5: 5})}, 2: {}}
    test_failed = check_for_failure(result, expected_result) or test_failed

    # RPC with Multi type
    multi = Xtruct()
    multi.string_thing = "Hello2"
    multi.byte_thing = 42
    multi.i32_thing = 4242
    multi.i64_thing = 424242
    result = await client.testMulti(ctx, 42, 4242, 424242, {1: "blah", 2: "thing"}, Numberz.EIGHT, 24)
    test_failed = check_for_failure(result, multi) or test_failed


    # RPC with Exception
    message = "Xception"
    try:
        result = await client.testException(ctx, message)
    except Xception as exception:
        if exception.errorCode != 1001 or exception.message != "Xception":
            print("\nUnexpected result {}".format(result), end="")
            test_failed = True

    # RPC with MultiException
    message = "Xception2"
    try:
        result = await client.testMultiException(ctx, message, "ignoreme")
        print("\nUnexpected result {}".format(result), end="")
        test_failed = True
    except Xception as exception:
        print("\nUnexpected result {}".format(exception), end="")
        test_failed = True
    except Xception2 as exception:
        if exception.errorCode != 2002 or exception.struct_thing.string_thing != "This is an Xception2":
            print("\nUnexpected result {}".format(exception), end="")
            test_failed = True

    # oneWay RPC call (no response)
    seconds = 1
    try:
        client.testOneway(ctx, seconds)
    except Exception as e:
        print("Unexpected error in testOneway() call: {}".format(e))
        test_failed = True

    if test_failed:
        exit(1)







if __name__ == '__main__':
    io_loop = asyncio.get_event_loop()
    io_loop.run_until_complete(main())
