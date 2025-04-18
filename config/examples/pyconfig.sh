#!/bin/bash

ROOT_PATH=$(dirname "$(realpath "${BASH_SOURCE[0]}")")

MODULE_NAME="${1}"
CONFIG_NAME="${2}"
SUB_FOLDER="${3:-1}"

WORK_DIR="${ROOT_PATH}/workdir/${CONFIG_NAME}/${SUB_FOLDER}"
rm -Rf "${WORK_DIR}" && mkdir -p "${WORK_DIR}"

eval cd "${ROOT_PATH}/../main" && \
  python3 -m "${MODULE_NAME}" "${WORK_DIR}" "${ROOT_PATH}/files/${CONFIG_NAME}.yaml"