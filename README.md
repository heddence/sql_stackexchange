# SQL StackExchange Project

## Overview

This project is designed for managing and querying data within
a PostgreSQL database, with a Dockerized environment and Conda-based
dependency management. The primary goal is to provide an API
to interact with SQL data, along with database restoration and
initialization capabilities.

## Features

* Dockerized PostgreSQL and application environment
* Pydantic schemas for data validation
* API for interacting with the database

## Project Structure

```plaintext
app/
├── api/                   # API endpoint definitions
│   ├── __init__.py        
│   └── endpoints.py       # Individual files for API routes
├── db/                    # Database session management
│   ├── __init__.py        
│   └── session.py         # Session handling for connecting to PostgreSQL
├── schemas/               # Pydantic schemas for data validation
│   ├── __init__.py
│   └── sql.py             # Individual files for schemas
├── services/              # Core service files for SQL query execution
│   ├── __init__.py
│   └── services.py        # Individual file for each endpoint
├── utils/
│   ├── __init__.py
│   └── sql.py             # Helper function, SQL reading utility
├── main.py                # Main entry point for the application
├── __init__.py            
data/                      # Contains data backups
│   └── superuser.backup   # Database backup file
sql_queries/               # Directory for SQL scripts and queries
│   └── superuser.backup   # Individual query for each endpoint
.env.example               # Sample environment file
.gitattributes             # Git configuration file (LFS)
.gitignore                 # Git ignore file
docker-compose.yml         # Docker Compose configuration
Dockerfile                 # Docker setup for application container
entrypoint.sh              # Initialization script for Conda in Docker
environment.yml            # Conda environment configuration
start.sh                   # Script for starting and initializing the application
README.md                  # Project documentation
```

## Setup and Installation

1. **Clone the Repository**:

```bash
git clone https://github.com/heddence/sql_stackexchange
```

2. **Set Up Environment Variables**: Copy .env.example to .env 
and update required values.

```bash
cp .env.example .env
```

```env
DB_USER=<user>
DB_PASSWORD=<password>
DB_NAME=<db_name>
DB_PORT=<db_port>
```

3. **Build and Start Docker Services**: Use the `start.sh` script to 
build Docker images, check the database, restore the backup if needed,
and bring up the application.

## Environment Variables

Specify each environment variable and its purpose:

* **DB_USER**: Database username for PostgreSQL.
* **DB_PASSWORD**: Password for the PostgreSQL user.
* **DB_NAME**: Name of the PostgreSQL database.
* **DB_PORT**: Port for PostgreSQL.
* **DB_HOST**: Hostname for connecting to the PostgreSQL database
(db is default, name of database docker container).

## Running the Application

The `start.sh` script automates the setup:

* **Database Service**: Builds and starts the database service
in Docker.
* **Database Check and Restoration**: Checks if the database is empty
and restores from `superuser.backup` if needed.
* **Application Service**: Starts the main application service.

After running `./start.sh`, the application should be accessible at the specified host and port.

## API Documentation

TODO

## Database Structure

The database used in this project is the reduced database from
StackExchange dump.

https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede/2678#2678