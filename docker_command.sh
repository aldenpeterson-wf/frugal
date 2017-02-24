#!/usr/bin/env bash

docker run  -v "${PWD}":"/scripts" google/dart:1.17.1 /scripts/scripts.sh
