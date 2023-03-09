#!/bin/bash
set -e

psqlasdasd -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

CREATE SCHEMA IF NOT EXISTS scrapper;

CREATE TABLE IF NOT EXISTS scrapper.enter_table_name_here (
	last_update varchar null,
    listingid varchar PRIMARY KEY,
);
EOSQL