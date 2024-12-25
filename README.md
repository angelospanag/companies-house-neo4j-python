# companies-house-neo4j-python

A proof of concept app that stores the full graph network (officers, persons with significant control) of a UK company
in
Neo4j using
the [Companies House Public Data API](https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference).

## Prerequisites

- [Python 3.13.\*](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/)

### 1. Install Python 3 and uv

**MacOS (using `brew`)**

```bash
brew install python3 uv
```

**Ubuntu/Debian**

```bash
sudo apt install python3 python3-venv
curl -LsSf https://astral.sh/uv/install.sh | sh
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
