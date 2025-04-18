#!/bin/bash

docker run --rm \
  -v ./workdir/docker:/data \
  -v ./files/localhost.yaml:/app/cloud-vpn.yaml \
  cloud-vpn:local