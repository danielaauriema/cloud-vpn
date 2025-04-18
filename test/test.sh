#!/bin/bash
set -e

SCRIPT_PATH=$(dirname "$(realpath "${BASH_SOURCE[0]}")")

. "${SCRIPT_PATH}/bash-utils.sh"

print_header "Cloud Setup Integration Test"

#-----------------------------------------------------------------------------------------------------------------------
# BUILD IMAGES
#-----------------------------------------------------------------------------------------------------------------------

print_header "Build Images"

print_section "build Cloud Config image"
docker build -f ../docker/config/Dockerfile -t cloud-config:test ../

print_section "pull and build Docker Compose images"
docker compose pull
docker compose build

#-----------------------------------------------------------------------------------------------------------------------
# TEST CREATE CONFIGS
#-----------------------------------------------------------------------------------------------------------------------
. ./test-config.sh

#-----------------------------------------------------------------------------------------------------------------------
# START DOCKER CONTAINERS AND INSTALL UTILITIES
#-----------------------------------------------------------------------------------------------------------------------

print_header "Start docker compose and install utilities"

print_section "start docker compose"
docker compose up -d

print_section "install dnsutils in bind9 container"
docker exec -t test_bind9 /bin/bash -c "apt update && apt install -y dnsutils"

print_section "install required tools in test_client"
docker exec -t test_client apk add curl

#-----------------------------------------------------------------------------------------------------------------------
# RUN TESTS
#-----------------------------------------------------------------------------------------------------------------------

print_header "Start integration tests"

#-----------------------------------------------------------------------------------------------------------------------
# TEST BIND9
#-----------------------------------------------------------------------------------------------------------------------

test_label "Bind9 :: test DNS server for nginx.${DOMAIN}"
test_assert "docker exec -t test_bind9 dig +noall +answer nginx.${DOMAIN} '@127.0.0.1' | grep -E '172.21.0.132'"

#-----------------------------------------------------------------------------------------------------------------------
# TEST NGINX
#-----------------------------------------------------------------------------------------------------------------------

test_label "Nginx :: test static site in localhost:82"
test_assert "docker exec -t test_nginx /bin/bash -c 'curl --fail -s localhost:82 | grep hello'"

#-----------------------------------------------------------------------------------------------------------------------
# TEST WIREGUARD
#-----------------------------------------------------------------------------------------------------------------------

test_label "Wireguard :: test Wireguard connection (ping)"
test_assert docker exec test_client ping -q -c 1 172.21.0.1

test_label "Wireguard :: test nginx connection/routing with curl:: 172.21.0.132:82"
test_assert "docker exec -t test_client /bin/bash -c 'curl --fail -s 172.21.0.132:82 | grep hello'"

test_label "Wireguard :: test nginx with curl + DNS :: nginx.${DOMAIN}"
test_assert "docker exec -t test_client /bin/bash -c 'curl --fail -s ${DOMAIN}:82| grep hello'"

#-----------------------------------------------------------------------------------------------------------------------
# TEAR DOWN
#-----------------------------------------------------------------------------------------------------------------------

print_header "Stopping containers"
docker compose down

print_header "Tests finished successfully"
