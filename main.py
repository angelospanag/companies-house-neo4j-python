import typer

from src.graph import store_in_neo4j


def main(company_number: str):
    store_in_neo4j(company_number)
    print(f"Storing company {company_number} data in Neo4j completed")


if __name__ == "__main__":
    typer.run(main)
