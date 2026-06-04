import os

os.environ.setdefault("COMPANIES_HOUSE_API_KEY", "test_key")
os.environ.setdefault(
    "COMPANIES_HOUSE_BASE_URL", "https://api.company-information.service.gov.uk/"
)
os.environ.setdefault("NEO4J_URI", "bolt://localhost:7687")
os.environ.setdefault("NEO4J_USER", "neo4j")
os.environ.setdefault("NEO4J_PASSWORD", "password")
