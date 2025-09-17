#!/bin/bash

# JobSift Database Initialization Script
# This script is run when the PostgreSQL container starts for the first time

set -e

# Create the main database if it doesn't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create extensions if needed
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pg_trgm";
    
    -- Create indexes for better performance (will be created by migrations)
    -- This is just a placeholder for future optimizations
    
    -- Set timezone
    SET timezone = 'UTC';
    
    -- Log initialization
    \echo 'JobSift database initialized successfully'
EOSQL

# Create test database for running tests
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE jobsift_test;
    GRANT ALL PRIVILEGES ON DATABASE jobsift_test TO $POSTGRES_USER;
    \echo 'JobSift test database created'
EOSQL

echo "JobSift PostgreSQL initialization completed"
