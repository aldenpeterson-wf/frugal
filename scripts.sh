#!/usr/bin/env bash
set -ex

export FRUGAL_HOME=/frugal

# Dart Dependencies
#cd $FRUGAL_HOME/test/integration/dart/test_client
#rm -rf .packages packages
cd $FRUGAL_HOME
pub upgrade
pub get --offline

# Run cross tests - want to report any failures, so don't allow command to exit
# without cleaning up
cd ${FRUGAL_HOME}

sleep 15
if go run test/integration/test.go test/integration/tests.json; then
    /testing/scripts/skynet/test_cleanup.sh
else
    /testing/scripts/skynet/test_cleanup.sh
    exit 1
fi