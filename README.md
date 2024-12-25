# companies-house-neo4j-python

A proof of concept app that stores the full graph network (officers, persons with significant control) of a UK company
in [Neo4j](https://neo4j.com) using
the [Companies House Public Data API](https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference).


<!-- TOC -->

* [companies-house-neo4j-python](#companies-house-neo4j-python)
    * [Prerequisites](#prerequisites)
        * [1. Install Python 3 and uv](#1-install-python-3-and-uv)
        * [2. Create a virtual environment with all necessary dependencies](#2-create-a-virtual-environment-with-all-necessary-dependencies)
        * [3. Create a `.env` file at the root of the project](#3-create-a-env-file-at-the-root-of-the-project)
        * [4. Optionally run a Neo4j database as a Docker container](#4-optionally-run-a-neo4j-database-as-a-docker-container)
    * [Run application](#run-application)
    * [Linting](#linting)
    * [Formatting](#formatting)

<!-- TOC -->

## Prerequisites

- [Python 3.13.\*](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/)

### 1. Install Python 3 and uv

**MacOS (using `brew`)**

```bash
brew install python@3.13 uv
```

**Ubuntu/Debian**

```bash
# Python
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv pipx
pipx ensurepath

# uv
pipx install uv
```

### 2. Create a virtual environment with all necessary dependencies

From the root of the project execute:

```bash
uv sync
```

### 3. Create a `.env` file at the root of the project

Generate an API key using
the [Companies House API guidelines](https://developer-specs.company-information.service.gov.uk/guides/authorisation).

```bash
COMPANIES_HOUSE_API_KEY="change_me"
COMPANIES_HOUSE_BASE_URL="https://api.company-information.service.gov.uk"

# Neo4j
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="your_password"
```

### 4. Optionally run a Neo4j database as a Docker container

```bash
docker compose up -d neo4j
```

## Run application

```bash
uv run main.py COMPANY_NUMBER
```

## Linting

```bash
uv run ruff check src/*
```

## Formatting

```bash
uv run ruff format src/*
```
