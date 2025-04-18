#!/bin/bash
set -e

if ! [ -f "${WG_CONFIG_SOURCE}" -o -d "${WG_CONFIG_SOURCE}" ]; then
  echo "** Waiting for configuration..."
  sleep 5s
fi

if [ -f "${WG_CONFIG_SOURCE}" ]; then
  echo "** Loading configuration from ${WG_CONFIG_SOURCE}"
  wg-quick up "${WG_CONFIG_SOURCE}"
elif [ -d "${WG_CONFIG_SOURCE}" ]; then
  echo ""
  for filename in "${WG_CONFIG_SOURCE}"/*.conf ; do
    wg-quick up "${filename}"
    echo ""
  done
else
  echo "** No configuration found."
  echo "WG_CONFIG_SOURCE = ${WG_CONFIG_SOURCE}"
fi

tail -f /dev/null
