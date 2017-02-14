/// Licensed to the Apache Software Foundation (ASF) under one
/// or more contributor license agreements. See the NOTICE file
/// distributed with this work for additional information
/// regarding copyright ownership. The ASF licenses this file
/// to you under the Apache License, Version 2.0 (the
/// 'License'); you may not use this file except in compliance
/// with the License. You may obtain a copy of the License at
///
/// http://www.apache.org/licenses/LICENSE-2.0
///
/// Unless required by applicable law or agreed to in writing,
/// software distributed under the License is distributed on an
/// 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
/// KIND, either express or implied. See the License for the
/// specific language governing permissions and limitations
/// under the License.

import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:args/args.dart';
import 'package:collection/collection.dart';
import 'package:thrift/thrift.dart';
import 'package:frugal_test/frugal_test.dart';
import 'package:frugal/frugal.dart';
import 'package:w_transport/w_transport.dart' as wt;
import 'package:w_transport/w_transport_vm.dart' show configureWTransportForVM;

typedef Future FutureFunction();

class FTest {
  final int errorCode;
  final String name;
  final FutureFunction func;

  FTest(this.errorCode, this.name, this.func);
}

class FTestError extends Error {
  final actual;
  final expected;

  FTestError(this.actual, this.expected);

  String toString() => '\n\nUNEXPECTED ERROR \n$actual != \n$expected\n\n';
}

List<FTest> _tests;
FFrugalTestClient client;
bool verbose;
FContext ctx;
var middleware_called = false;

main(List<String> args) async {
  configureWTransportForVM();
  ArgResults results = _parseArgs(args);

  if (results == null) {
    exit(1);
  }

  verbose = results['verbose'] == true;

  await _initTestClient(
      host: results['host'],
      port: int.parse(results['port']),
      transportType: results['transport'],
      protocolType: results['protocol']).catchError((e) {
    stdout.writeln('Error:');
    stdout.writeln('$e');
    if (e is Error) {
      stdout.writeln('${e.stackTrace}');
    }
    exit(1);
  });

  // run tests
  int result = 0;
  _tests = _createTests();

  for (FTest test in _tests) {
    if (verbose) stdout.write('${test.name}... ');
    try {
      await test.func();
      if (verbose) stdout.writeln('success!');
    } catch (e) {
      stdout.writeln(e.toString());
      result = result | test.errorCode;
    }
  }

  if (middleware_called) {
    stdout.writeln("Middleware successfully called.");
  } else {
    stdout.writeln("Middleware never called!");
    result = 1;
  }

  exit(result);
}

ArgResults _parseArgs(List<String> args) {
  var parser = new ArgParser();
  parser.addOption('host', defaultsTo: 'localhost', help: 'The server host');
  parser.addOption('port', defaultsTo: '9090', help: 'The port to connect to');
  parser.addOption('transport',
      defaultsTo: 'http',
      allowed: ['http'],
      help: 'The transport name',
      allowedHelp: {
        'http': 'http transport'
      });
  parser.addOption('protocol',
      defaultsTo: 'binary',
      allowed: ['binary', 'compact', 'json'],
      help: 'The protocol name',
      allowedHelp: {
        'binary': 'TBinaryProtocol',
        'compact': 'TCompactProtocol',
        'json': 'TJsonProtocol'
      });
  parser.addFlag('verbose', defaultsTo: false);

  ArgResults results;
  try {
    results = parser.parse(args);
  } catch (e) {
    stdout.writeln('$e\n');
  }

  if (results == null) stdout.write(parser.usage);

  return results;
}

TProtocolFactory getProtocolFactory(String protocolType) {
  if (protocolType == 'binary') {
    return new TBinaryProtocolFactory();
  } else if (protocolType == 'compact') {
    return new TCompactProtocolFactory();
  } else if (protocolType == 'json') {
    return new TJsonProtocolFactory();
  }

  throw new ArgumentError.value(protocolType);
}

Middleware clientMiddleware() {
  return (InvocationHandler next) {
    return (String serviceName, String methodName, List<Object> args) {
      stdout.write(methodName + "(" + args.sublist(1).toString() + ") = ");
      middleware_called = true;
      return next(serviceName, methodName, args).then((result) {
        stdout.write(result.toString() + '\n');
        return result;
      }).catchError((e) {
        stdout.write(e.toString() + '\n');
        throw e;
      });
    };
  };
}

Future _initTestClient(
    {String host, int port, String transportType, String protocolType}) async {

  FProtocolFactory fProtocolFactory = null;
  FTransport transport = null;
  ctx = new FContext();

//  Nats is not available without the SDK in dart, so HTTP is the only transport we can test
  var uri = Uri.parse('http://$host:$port');
  transport = new FHttpTransport(new wt.Client(), uri);
  await transport.open();

  fProtocolFactory = new FProtocolFactory(getProtocolFactory(protocolType));
  client = new FFrugalTestClient(new FServiceProvider(transport, fProtocolFactory), [clientMiddleware()]);
}

List<FTest> _createTests() {
  List<FTest> tests = [];

  var xtruct = new Xtruct()
    ..string_thing = 'Zero'
    ..byte_thing = 1
    ..i32_thing = -3
    ..i64_thing = -5;

  tests.add(new FTest(1, 'testVoid', () async {
    await client.testVoid(ctx);
  }));

  tests.add(new FTest(1, 'testString', () async {
    var input = 'Test';
    var result = await client.testString(ctx, input);
    if (result != input) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testBool', () async {
    var input = true;
    var result = await client.testBool(ctx, input);
    if (result != input) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testByte', () async {
    var input = 64;
    var result = await client.testByte(ctx, input);
    if (result != input) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testI32', () async {
    var input = 2147483647;
    var result = await client.testI32(ctx, input);
    if (result != input) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testI64', () async {
    var input = 9223372036854775807;
    var result = await client.testI64(ctx, input);
    if (result != input) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testDouble', () async {
    var input = 3.1415926;
    var result = await client.testDouble(ctx, input);
    if (result != input) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testBinary', () async {
    var utf8Codec = const Utf8Codec();
    var input = utf8Codec.encode('foo');
    var result = await client.testBinary(ctx, input);
    var equality = const ListEquality();
    if (!equality.equals(result, input)) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testStruct', () async {
    var result = await client.testStruct(ctx, xtruct);
    if ('$result' != '$xtruct') throw new FTestError(result, xtruct);
  }));

  tests.add(new FTest(1, 'testNest', () async {
    var input = new Xtruct2()
      ..byte_thing = 1
      ..struct_thing = xtruct
      ..i32_thing = -3;

    stdout.write("testNest(${input})");
    var result = await client.testNest(ctx, input);
    if ('$result' != '$input') throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testMap', () async {
    Map<int, int> input = {1: -10, 2: -9, 3: -8, 4: -7, 5: -6};

    var result = await client.testMap(ctx, input);
    var equality = const MapEquality();
    if (!equality.equals(result, input)) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testSet', () async {
    var input = new Set.from([-2, -1, 0, 1, 2]);
    var result = await client.testSet(ctx, input);
    var equality = const SetEquality();
    if (!equality.equals(result, input)) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testList', () async {
    var input = [-2, -1, 0, 1, 2];
    var result = await client.testList(ctx, input);
    var equality = const ListEquality();
    if (!equality.equals(result, input)) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testEnum', () async {
    await _testEnum(Numberz.ONE);
    await _testEnum(Numberz.TWO);
    await _testEnum(Numberz.THREE);
    await _testEnum(Numberz.FIVE);
    await _testEnum(Numberz.EIGHT);
  }));

  tests.add(new FTest(1, 'testTypedef', () async {
    var input = 309858235082523;
    var result = await client.testTypedef(ctx, input);
    if (result != input) throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testMapMap', () async {
    Map<int, Map<int, int>> result = await client.testMapMap(ctx, 1);
    if (result.isEmpty || result[result.keys.first].isEmpty) {
      throw new FTestError(result, 'Map<int, Map<int, int>>');
    }
  }));

  tests.add(new FTest(1, 'testUppercaseMethod', () async {
    var input = true;
    var result = await client.testUppercaseMethod(ctx, input);
    if (result != input) throw new FTestError(result, input);
  }));


  tests.add(new FTest(1, 'testInsanity', () async {
    var input = new Insanity();
    input.userMap = {Numberz.FIVE: 5000};
    input.xtructs = [xtruct];

    Map<int, Map<int, Insanity>> result = await client.testInsanity(ctx, input);
    if (result.isEmpty || result[1].isEmpty) {
      throw new FTestError(result, input);
    }
  }));

  tests.add(new FTest(1, 'testMulti', () async {
    var input = new Xtruct()
      ..string_thing = 'Hello2'
      ..byte_thing = 123
      ..i32_thing = 456
      ..i64_thing = 789;

    var result = await client.testMulti(ctx, input.byte_thing, input.i32_thing,
        input.i64_thing, {1: 'one'}, Numberz.EIGHT, 5678);
    if ('$result' != '$input') throw new FTestError(result, input);
  }));

  tests.add(new FTest(1, 'testException', () async {
    try {
      await client.testException(ctx, 'Xception');
    } on Xception catch (exception) {
      return;
    }

    throw new FTestError(null, 'Xception');
  }));

  tests.add(new FTest(1, 'testMultiException', () async {
    try {
      await client.testMultiException(ctx, 'Xception2', 'foo');
    } on Xception2 catch (exception2) {
      return;
    }

    throw new FTestError(null, 'Xception2');
  }));

  tests.add(new FTest(1, 'testOneway', () async {
      await client.testOneway(ctx, 1);
  }));

  tests.add(new FTest(1, 'testUncheckedException', () async {
      try {
        await client.testUncaughtException(ctx);
      } on TApplicationError catch (e) {

        if (e.type != FrugalTApplicationErrorType.INTERNAL_ERROR ||
            !e.message.contains('An uncaught error')){
          throw new FTestError(e, TApplicationError(FrugalTApplicationErrorType.INTERNAL_ERROR));
        }
      }}));

  tests.add(new FTest(1, 'testUncheckedTApplicationException', () async {
      try {
        await client.testUncheckedTApplicationException(ctx);
      } on TApplicationError catch (e) {
        int expectedErrorType = 400;
        if (e.type != expectedErrorType ||
            !e.message.contains('Unchecked TApplicationException')) {
          throw new FTestError(e, TApplicationError(expectedErrorType));
        }
      }}));

  return tests;
}

Future _testEnum(int input) async {
  var result = await client.testEnum(ctx, input);
  if (result != input) throw new FTestError(result, input);
}
