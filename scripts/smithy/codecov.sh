#!/bin/bash

echo "\nRunning codecov"
if [ -z "$GIT_BRANCH" ]
then
	echo "GIT_BRANCH environment variable not set, skipping codecov push"
else
	TRACKING_REMOTE="$(git for-each-ref --format='%(upstream:short)' $(git symbolic-ref -q HEAD) | cut -d'/' -f1 | xargs git ls-remote --get-url | cut -d':' -f2 | sed 's/.git$//')"

	# Dart
	bash <(curl -s https://codecov.workiva.net/bash) -t $CODECOV_TOKEN -r $TRACKING_REMOTE -f $FRUGAL_HOME/lib/dart/coverage/coverage.lcov -F dartlibrarytest

	# Go library
    bash <(curl -s https://codecov.workiva.net/bash) -t $CODECOV_TOKEN -r $TRACKING_REMOTE -f $FRUGAL_HOME/gocoverage.txt -F golibrary

	# Java library
    bash <(curl -s https://codecov.workiva.net/bash) -t $CODECOV_TOKEN -r $TRACKING_REMOTE -f $FRUGAL_HOME/lib/java/target/site/jacoco/jacoco.xml -F java_library

    # Python2
    bash <(curl -s https://codecov.workiva.net/bash) -t $CODECOV_TOKEN -r $TRACKING_REMOTE -f $FRUGAL_HOME/lib/python/coverage_py2.xml -F python_two

fi
