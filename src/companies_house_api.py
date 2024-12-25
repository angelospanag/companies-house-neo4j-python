import requests

from src.config import get_settings


def get_company_data(company_number):
    """Fetch company data from Companies House API.

    Args:
        company_number: The company number
    """
    url = f"{get_settings().companies_house_base_url}company/{company_number}"
    try:
        response = requests.get(
            url, auth=(get_settings().companies_house_api_key.get_secret_value(), "")
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching company data: {e}")
        return None


def get_officers_data(company_number):
    """Fetch officers data for a company from Companies House API.

    Args:
        company_number: The company number
    """
    url = f"{get_settings().companies_house_base_url}company/{company_number}/officers"
    try:
        response = requests.get(
            url, auth=(get_settings().companies_house_api_key.get_secret_value(), "")
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching officers data: {e}")
        return None


def get_pscs_data(company_number):
    """Fetch persons with significant control data for a company.

    Args:
        company_number: The company number
    """
    url = f"{get_settings().companies_house_base_url}company/{company_number}/persons-with-significant-control"
    try:
        response = requests.get(
            url, auth=(get_settings().companies_house_api_key.get_secret_value(), "")
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching PSC data: {e}")
        return None
