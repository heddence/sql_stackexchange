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
DB_HOST_PORT=<db_host_port>

DB_PORT=5432
DB_HOST=db
```

3. **Build and Start Docker Services**: Use the `start.sh` script to 
build Docker images, check the database, restore the backup if needed,
and bring up the application.

## Environment Variables

Specify each environment variable and its purpose:

* **DB_USER**: Database username for PostgreSQL.
* **DB_PASSWORD**: Password for the PostgreSQL user.
* **DB_NAME**: Name of the PostgreSQL database.
* **DB_HOST_PORT**: Port on the host machine.
* **DB_PORT**: Port for PostgreSQL (Default port 5432, **must not be
changed**).
* **DB_HOST**: Hostname for connecting to the PostgreSQL database
(db is default, name of database docker container,
**must not be changed**).

## Running the Application

The `start.sh` script automates the setup:

* **Database Service**: Builds and starts the database service
in Docker.
* **Database Check and Restoration**: Checks if the database is empty
and restores from `superuser.backup` if needed.
* **Application Service**: Starts the main application service.

After running `./start.sh`, the application should be accessible at the specified host and port.

## API Documentation

* GET `/v2/posts/:post_id/users`: Return a list of all discussants (users) of the post (posts)
with the ID :post_id, sorting them according to when their comment was made,
starting with the newest and ending with the oldest.
* GET `/v2/users/:user_id/friends`: Produce a discussion list for the :user_id, containing users
who have commented on posts that the user has created or commented on.
* GET `/v2/tags/:tagname/stats`: Determine the percentage of posts with a particular :tagname within
the total number of posts published on each day of the week (e.g. Monday, Tuesday),
for each day of the week separately. Show the results on a scale of 0 - 100 and round to two
decimal places.
* GET `/v2/posts/q1/?duration=:duration_in_minutes&limit=:limit`: The output is a list of the :limit
of the most recently resolved posts that have been opened for a maximum of :duration_in_minutes
(the number of minutes between creationdate and closeddate). Round the opening duration to two 
decimal places.
* GET `/v2/posts/q2/?limit=:limit&query=:query`: Provide a list of posts that contain :query,
ordered from newest to oldest. Limit output to :limit. Include a complete list of associated 
tags as part of the response.
* GET `/v2/users/:user_id/badge_history`: For the selected user with :user_id, analyze the badges he/she
has earned by outputting all the badges he/she has earned, along with the previous report the author
wrote before earning the badge. If he has earned a badge and no message has been sent before the badge,
the badge will not be displayed in the output. For example, if he has earned 2 badges and several
messages have been sent before, then only the last badge is displayed in the output, with the last
message preceding it being shown.
* GET `/v2/tags/:tagname/comments?count=:count`: For a given :tagname, calculate the average response
time between comments for individual posts that have more than the specified number of comments :count
within that post. In the output, indicate how the individual average response time changed as more
comments were added.
* GET `/v2/tags/:tagname/comments/:position?limit=:limit`: Return comments for posts with the :tagname 
that were created as k's in order (:position) sorted by creation date procedure with :limit.
* GET `/v2/posts/:postid?limit=:limit`: The output is a list of :limit size for the post with
:postid. The thread starts with :postid and continues with posts, where :postid is a parentid 
sorted by creation date starting from the oldest.

## Database Structure

The database used in this project is the reduced database from
StackExchange dump.

https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede/2678#2678

Tables:
* **badges**
* **comments**
* **post_history**
* **post_link**
* **post_tags**
* **posts**
* **tags**
* **users**
* **votes**
