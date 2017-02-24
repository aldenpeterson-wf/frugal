#!/usr/bin/env bash
set -ex

cd /z

# Run pub upgrade a few times to likely fail it
pub upgrade
pub upgrade
pub upgrade
pub upgrade
pub upgrade
pub upgrade
pub upgrade
pub upgrade


sleep 60