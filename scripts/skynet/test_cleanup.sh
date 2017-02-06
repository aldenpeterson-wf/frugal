#!/usr/bin/env bash
set -ex

lsof

cd $GOPATH/src/github.com/Workiva/frugal
FRUGAL_HOME=$GOPATH/src/github.com/Workiva/frugal

# tar the test logs for storage
tar -czf test_logs.tar.gz test/integration/log
mv test_logs.tar.gz /testing/artifacts/

pkill gnatsd
