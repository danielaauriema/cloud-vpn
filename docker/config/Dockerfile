ARG BASE_IMAGE=alpine:3.21.3
FROM ${BASE_IMAGE}

ARG PKG_UPDATE="apk update"
ARG PKG_TOOLS="apk add --no-cache gnutls-utils wireguard-tools-wg-quick"
ARG PKG_PYTHON3="apk add --no-cache python3 py3-jinja2 py3-netaddr py3-yaml py3-dotenv"

ENV CLOUD_VPN_CONFIG="/app/config.yaml"
ENV CLOUD_VPN_WORKDIR="/data"

ENV PYTHONUNBUFFERED=1
RUN ${PKG_UPDATE} && ${PKG_TOOLS} && ${PKG_PYTHON3} && ln -sf python3 /usr/bin/python && mkdir /app
WORKDIR /app

COPY ./config/main  /app
COPY ./docker/config/entrypoint.sh  /app/entrypoint
RUN chmod ugo+x /app/entrypoint

ENTRYPOINT []
CMD ["/app/entrypoint"]
