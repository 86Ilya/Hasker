FROM postgres:9.6-alpine

COPY build/db_service/init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh
COPY build/db_service/hasker_db_dump /hasker_db_dump
RUN chmod a+r /docker-entrypoint-initdb.d/*
