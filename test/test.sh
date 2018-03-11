#!/bin/bash
self_dir="$(dirname "$(readlink -f "$0")")"
cd "${self_dir}"

python test.py
