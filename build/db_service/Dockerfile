FROM postgres:9.6-alpine

COPY build/db_service/init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh
RUN chmod a+r /docker-entrypoint-initdb.d/*
