FROM perl:5.42-slim-trixie

RUN groupadd --gid 999 pgbadger \
    && useradd --uid 999 --gid 999 --home-dir /app --create-home pgbadger \
    && mkdir -p /app/logs /app/reports \
    && chown -R 999:999 /app \
    && apt-get update \
    && apt-get install -y --no-install-recommends pgbadger \
    && rm -rf /var/lib/apt/lists/*

COPY scripts/pgbadger-entrypoint.sh /usr/local/bin/pgbadger-entrypoint
RUN chmod 0755 /usr/local/bin/pgbadger-entrypoint

USER 999:999
ENTRYPOINT ["/usr/local/bin/pgbadger-entrypoint"]
