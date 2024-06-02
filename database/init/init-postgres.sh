#!/bin/bash
set -e

sed -e "s/\${PG_USER}/$PG_USER/" -e "s/\${PG_PASSWORD}/$PG_PASSWORD/" -e "s/\${POSTGRES_DB}/$POSTGRES_DB/" /tmp/init-postgres-tmp.sql > /tmp/init-postgres.sql

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /tmp/init-postgres.sql
