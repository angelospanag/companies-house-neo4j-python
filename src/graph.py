from neo4j import GraphDatabase

from src.companies_house_api import get_company_data, get_officers_data, get_pscs_data
from src.config import get_settings

visited_companies = set()  # To prevent processing the same company multiple times


def store_in_neo4j(company_number):
    """Fetch and store company, officers, and PSC data recursively in Neo4j."""
    if company_number in visited_companies:
        print(f"Company {company_number} already processed, skipping.")
        return

    visited_companies.add(company_number)

    company_data = get_company_data(company_number)
    officers_data = get_officers_data(company_number)
    pscs_data = get_pscs_data(company_number)

    if company_data:
        driver = GraphDatabase.driver(
            str(get_settings().neo4j_uri),
            auth=(get_settings().neo4j_user, get_settings().neo4j_password.get_secret_value()),
        )
        with driver.session() as session:
            session.write_transaction(create_company_node, company_data)

            if officers_data and "items" in officers_data:
                for officer in officers_data["items"]:
                    session.write_transaction(
                        create_officer_or_corporate_officer, company_data, officer
                    )

                    # Recursively fetch data for corporate officers
                    if officer.get("is_corporate_officer", False):
                        corporate_number = officer.get("identification", {}).get(
                            "registration_number"
                        )
                        if corporate_number:
                            store_in_neo4j(corporate_number)

            if pscs_data and "items" in pscs_data:
                for psc in pscs_data["items"]:
                    session.write_transaction(
                        create_psc_node_and_relationship, company_data, psc
                    )

                    # Recursively fetch data for corporate PSCs
                    if (
                            psc.get("kind")
                            == "corporate-entity-person-with-significant-control"
                    ):
                        corporate_number = psc.get("identification", {}).get(
                            "registration_number"
                        )
                        if corporate_number:
                            store_in_neo4j(corporate_number)

        driver.close()


def create_company_node(tx, data):
    """Create a company node in Neo4j."""
    query = """
    MERGE (c:Company {company_number: $company_number})
    SET c.name = $name,
        c.status = $status,
        c.address = $address,
        c.incorporation_date = $incorporation_date
    """
    tx.run(
        query,
        company_number=data.get("company_number"),
        name=data.get("company_name"),
        status=data.get("company_status"),
        address=", ".join(data.get("registered_office_address", {}).values()),
        incorporation_date=data.get("date_of_creation"),
    )


def create_officer_or_corporate_officer(tx, company_data, officer_data):
    """Create an officer node (individual or corporate) and link to the company."""
    if officer_data.get("is_corporate_officer", False):
        # Corporate officer
        query = """
        MERGE (co:Company {name: $name})
        SET co.company_number = $company_number
        WITH co
        MATCH (c:Company {company_number: $company_number_main})
        MERGE (c)-[:HAS_CORPORATE_OFFICER]->(co)
        """
        tx.run(
            query,
            name=officer_data.get("name"),
            company_number=officer_data.get("identification", {}).get(
                "registration_number"
            ),
            company_number_main=company_data.get("company_number"),
        )
    else:
        # Individual officer
        query = """
        MERGE (o:Officer {name: $name, officer_id: $officer_id})
        SET o.appointed_on = $appointed_on,
            o.resigned_on = $resigned_on,
            o.role = $role
        WITH o
        MATCH (c:Company {company_number: $company_number})
        MERGE (c)-[:HAS_OFFICER]->(o)
        """
        tx.run(
            query,
            name=officer_data.get("name"),
            officer_id=officer_data.get(
                "officer_id", officer_data.get("name")
            ),  # Fallback to name if no ID
            appointed_on=officer_data.get("appointed_on"),
            resigned_on=officer_data.get("resigned_on"),
            role=officer_data.get("officer_role"),
            company_number=company_data.get("company_number"),
        )


def create_psc_node_and_relationship(tx, company_data, psc_data):
    """Create PSC node (individual or corporate) and link to the company."""
    if psc_data.get("kind") == "corporate-entity-person-with-significant-control":
        # Corporate PSC
        query = """
        MERGE (psc:Company {name: $name})
        SET psc.company_number = $company_number
        WITH psc
        MATCH (c:Company {company_number: $company_number_main})
        MERGE (c)-[:HAS_CORPORATE_PSC]->(psc)
        """
        tx.run(
            query,
            name=psc_data.get("name"),
            company_number=psc_data.get("identification", {}).get(
                "registration_number"
            ),
            company_number_main=company_data.get("company_number"),
        )
    else:
        # Individual PSC
        query = """
        MERGE (psc:Individual {name: $name, psc_id: $psc_id})
        SET psc.notified_on = $notified_on,
            psc.ceased_on = $ceased_on
        WITH psc
        MATCH (c:Company {company_number: $company_number})
        MERGE (c)-[:HAS_PSC]->(psc)
        """
        tx.run(
            query,
            name=psc_data.get("name"),
            psc_id=psc_data.get("links", {}).get("self"),
            notified_on=psc_data.get("notified_on"),
            ceased_on=psc_data.get("ceased_on"),
            company_number=company_data.get("company_number"),
        )
