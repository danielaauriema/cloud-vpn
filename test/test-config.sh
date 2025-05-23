#!/bin/bash
set -e

SCRIPT_PATH=$(dirname "$(realpath "${BASH_SOURCE[0]}")")

CACHE_PATH="${SCRIPT_PATH}/.cache"
BASH_UTILS="${CACHE_PATH}/bash-utils.sh"
if [ ! -f "$BASH_UTILS" ]; then
  mkdir -p "${CACHE_PATH}"
  curl -s "https://raw.githubusercontent.com/danielaauriema/cloud-utils/refs/heads/main/bash/src/bash-utils.sh" > "${BASH_UTILS}"
fi
# shellcheck disable=SC1090
. "${BASH_UTILS}"

. .env

print_header "Cloud Config Test"

rm -Rf "${WORK_DIR}" && mkdir -p "${WORK_DIR}"

print_header "generate configs"
docker run --rm -v "${WORK_DIR}:/data" \
  -v "./files/${CONFIG}.yaml:/app/config.yaml" \
  cloud-config:test

test_files "${WORK_DIR}/${DNS_DIR}/${DOMAIN}" \
  "${WORK_DIR}/${DNS_DIR}/named.conf" \
  "${WORK_DIR}/${DNS_DIR}/named.conf.options" \
  "${WORK_DIR}/${NGINX_DIR}/default.conf" \
  "${WORK_DIR}/${NGINX_DIR}/hello.conf" \
  "${WORK_DIR}/${NGINX_DIR}/redirect_https.conf" \
  "${WORK_DIR}/${NGINX_DIR}/site_https.conf" \
  "${WORK_DIR}/${SSL_DIR}/${CONFIG}/ca/${CONFIG}.crt" \
  "${WORK_DIR}/${SSL_DIR}/${CONFIG}/ca/${CONFIG}.key" \
  "${WORK_DIR}/${SSL_DIR}/${CONFIG}/certs/${DOMAIN}.crt" \
  "${WORK_DIR}/${SSL_DIR}/${CONFIG}/certs/${DOMAIN}.key" \
  "${WORK_DIR}/${WG_DIR}/conf/_servers/wg0.conf" \
  "${WORK_DIR}/${WG_DIR}/conf/test_client/wg0.conf"