#!/usr/bin/env bash
set -ex

cd /scripts

# Run pub upgrade a few times to likely somewhere catastrophically
pub upgrade
pub upgrade
pub upgrade
pub upgrade
pub upgrade
pub upgrade
pub upgrade
pub upgrade


sleep 60