#!/usr/bin/env bash
set -ex

export FRUGAL_HOME=/frugal

# Dart Dependencies
#cd $FRUGAL_HOME/test/integration/dart/test_client
#rm -rf .packages packages
cd $FRUGAL_HOME
pub upgrade
#pub get --offline -v

# Run cross tests - want to report any failures, so don't allow command to exit
# without cleaning up
cd ${FRUGAL_HOME}

sleep 60