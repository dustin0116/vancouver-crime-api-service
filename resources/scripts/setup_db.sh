#!/bin/bash

source ../../.env

echo "Setting up PostgreSQL database..."

# Create user and database using env variables
psql postgres <<EOF
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$DB_USERNAME') THEN
    CREATE ROLE $DB_USERNAME WITH LOGIN PASSWORD '$DB_PASSWORD';
  END IF;
END
\$\$;

ALTER ROLE $DB_USERNAME CREATEDB;

-- Drop database if it exists and create new one
DROP DATABASE IF EXISTS $DB_NAME;
CREATE DATABASE $DB_NAME OWNER $DB_USERNAME;

GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USERNAME;

\c $DB_NAME

-- Create schema if you're using one
CREATE SCHEMA IF NOT EXISTS public AUTHORIZATION $DB_USERNAME;
GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USERNAME;
EOF

echo "Database setup completed!"