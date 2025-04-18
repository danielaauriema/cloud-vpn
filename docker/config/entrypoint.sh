#!/bin/bash
set -e

mkdir -p "${CLOUD_VPN_WORKDIR}/dns" \
  "${CLOUD_VPN_WORKDIR}/nginx" \
  "${CLOUD_VPN_WORKDIR}/ssl" \
  "${CLOUD_VPN_WORKDIR}/wireguard"

python3 -m "pydns" "${CLOUD_VPN_WORKDIR}/dns" "${CLOUD_VPN_CONFIG}"
python3 -m "pynginx" "${CLOUD_VPN_WORKDIR}/nginx" "${CLOUD_VPN_CONFIG}"
python3 -m "pyssl" "${CLOUD_VPN_WORKDIR}/ssl" "${CLOUD_VPN_CONFIG}"
python3 -m "pywg" "${CLOUD_VPN_WORKDIR}/wireguard" "${CLOUD_VPN_CONFIG}"

echo "** vpn config finished"