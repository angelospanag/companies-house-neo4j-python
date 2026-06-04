from unittest.mock import MagicMock, patch

import requests

from src.companies_house_api import get_company_data, get_officers_data, get_pscs_data


def test_get_company_data_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "company_number": "00610095",
        "company_name": "Test Company",
    }
    with patch("src.companies_house_api.requests.get", return_value=mock_response):
        result = get_company_data("00610095")
    assert result == {"company_number": "00610095", "company_name": "Test Company"}


def test_get_company_data_request_error():
    with patch(
        "src.companies_house_api.requests.get",
        side_effect=requests.RequestException("connection error"),
    ):
        result = get_company_data("00610095")
    assert result is None


def test_get_officers_data_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"items": [{"name": "John Smith"}]}
    with patch("src.companies_house_api.requests.get", return_value=mock_response):
        result = get_officers_data("00610095")
    assert result == {"items": [{"name": "John Smith"}]}


def test_get_pscs_data_request_error():
    with patch(
        "src.companies_house_api.requests.get",
        side_effect=requests.RequestException("timeout"),
    ):
        result = get_pscs_data("00610095")
    assert result is None
