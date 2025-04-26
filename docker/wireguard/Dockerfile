ARG BASE_IMAGE=alpine:3.21.3
FROM ${BASE_IMAGE}

ARG PKG_UPDATE="apk update"
ARG PKG_WIREGUARD="apk add --no-cache wireguard-tools-wg-quick iptables"

ENV WG_CONFIG_SOURCE="/etc/wireguard/wg0.conf"

RUN ${PKG_UPDATE} && ${PKG_WIREGUARD}

COPY ./docker/wireguard/entrypoint.sh /app/entrypoint
RUN chmod u+x /app/entrypoint

ENTRYPOINT []
CMD ["/app/entrypoint"]

