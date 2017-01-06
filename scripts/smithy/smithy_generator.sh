#!/usr/bin/env bash
set -e

# Run the generator tests
cd $FRUGAL_HOME
godep go build -o frugal
godep go test -race ./test
mv frugal $SMITHY_ROOT
rm -rf ./test/out

	common_test.go:48: Expected line
	<                e = _write_application_exception(ctx, oprot, "ping", ex_code=TApplicationException.UNKNOWN, message=e.message)> (expected/python.tornado/variety/f_Foo.py), generated line
	<                e = _write_application_exception(ctx, oprot, "ping", ex_type=TApplicationException.UNKNOWN, message=e.message)> (out/tornado/variety/python/f_Foo.py) at line 722
