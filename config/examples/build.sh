#!/bin/bash
set -e

CONFIG="${1:-example}"

./pyconfig.sh pydns   "${CONFIG}" dns
./pyconfig.sh pynginx "${CONFIG}" nginx
./pyconfig.sh pyssl   "${CONFIG}" ssl
./pyconfig.sh pywg    "${CONFIG}" wireguard
