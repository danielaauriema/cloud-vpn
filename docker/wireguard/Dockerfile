ARG BASE_IMAGE=alpine:3.21.3
FROM ${BASE_IMAGE}

ARG PKG_UPDATE="apk update"
ARG PKG_WIREGUARD="apk add --no-cache wireguard-tools-wg-quick iptables"

ENV WG_CONFIG_SOURCE="/etc/wireguard/wg0.conf"

RUN ${PKG_UPDATE} && ${PKG_WIREGUARD}

COPY ./docker/wireguard/entrypoint.sh /entrypoint
RUN chmod u+x /entrypoint

ENTRYPOINT [ "/bin/bash", "-c" ]
CMD ["/entrypoint"]

