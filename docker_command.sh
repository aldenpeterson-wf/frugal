#!/usr/bin/env bash

# docker run -it -v "/Users/aldenpeterson/.skynet-cli/.pub-cache":"/root/.pub-cache:rw"  -v "/Users/aldenpeterson/go/src/github.com/Workiva/frugal":"/frugal" drydock-prod.workiva.net/workiva/messaging-docker-images:119185 /bin/bash

docker run --name tester -it  -v "/Users/aldenpeterson/go/src/github.com/Workiva/frugal":"/frugal" drydock-prod.workiva.net/workiva/smithy-runner-dart:110229 /bin/bash
