
FROM ghcr.io/xtls/xray-core:latest AS xray

FROM alpine:3.22

RUN addgroup -g 65532 xray && \
    adduser -D -u 65532 -G xray xray

COPY --from=xray /usr/local/bin/xray /usr/local/bin/xray

COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

USER 65532:65532

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
