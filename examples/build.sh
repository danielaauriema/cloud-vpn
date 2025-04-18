#!/bin/bash
set -e

CONFIG="${1:-example}"
MODULE="${2}"

if [ -z "${MODULE}" -o "${MODULE}" == "pydns" ]; then
  ./pymodule.sh pydns   "${CONFIG}" dns
fi;
if [ -z "${MODULE}" -o "${MODULE}" == "pynginx" ]; then
  ./pymodule.sh pynginx "${CONFIG}" nginx
fi;
if [ -z "${MODULE}" -o "${MODULE}" == "pyssç" ]; then
  ./pymodule.sh pyssl   "${CONFIG}" ssl
fi;
if [ -z "${MODULE}" -o "${MODULE}" == "pywg" ]; then
  ./pymodule.sh pywg    "${CONFIG}" wireguard
fi;
