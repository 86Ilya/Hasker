#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
    CREATE USER hasker with password 'hasker' CREATEDB;
    CREATE DATABASE hasker_db;
    GRANT ALL PRIVILEGES ON DATABASE hasker_db TO hasker;
EOSQL
psql -U hasker -d hasker_db -q < /hasker_db_dump
