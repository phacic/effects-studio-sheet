import pathlib

import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from pytest_mock import MockerFixture


def test_get_data(api_client: APIClient, mocker: MockerFixture, generate_response_data, request_response, settings):
    resp_data = generate_response_data()
    mock = mocker.patch("urllib.request.urlopen")
    mock.return_value = request_response(resp_data=resp_data)

    url = reverse("sheet-view")

    resp = api_client.get(path=url)
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data
