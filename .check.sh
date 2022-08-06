#!/usr/bin/env bash

for f in * ; do echo "checking $f..."; fastd --verify-config --config-peer "$f" || exit 1; done
