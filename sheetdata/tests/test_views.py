import pathlib
from urllib.error import URLError

import pytest
from pytest_mock import MockerFixture
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


def test_get_data(
        api_client: APIClient,
        mocker: MockerFixture,
        generate_response_data,
        request_response
):
    resp_data = generate_response_data()
    mock = mocker.patch("urllib.request.urlopen")
    mock.return_value = request_response(resp_data=resp_data)

    url = reverse("sheet-view")

    resp = api_client.get(path=url)
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data


def test_get_data_nocache(
        api_client: APIClient,
        mocker: MockerFixture,
        generate_response_data,
        request_response,
        settings,
):
    resp_data = generate_response_data()
    mock = mocker.patch("urllib.request.urlopen")
    mock.return_value = request_response(resp_data=resp_data)

    url = reverse("sheet-view") + "?nocache=1"

    resp = api_client.get(path=url)
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data

    # cache file should not be present
    assert not pathlib.Path.exists(settings.SAVED_CSV_FILE_PATH)


def test_get_data_with_pagination(
        api_client: APIClient,
        mocker: MockerFixture,
        generate_response_data,
        request_response,
        settings,
):
    resp_data = generate_response_data()
    mock = mocker.patch("urllib.request.urlopen")
    mock.return_value = request_response(resp_data=resp_data)

    url = reverse("sheet-view") + "?page=1"

    resp = api_client.get(path=url)
    resp_data = resp.json()

    assert resp.status_code == 200
    assert len(resp_data) == 5


def test_get_data_404(
        api_client: APIClient,
        mocker: MockerFixture,
        generate_response_data,
        request_response,
        settings,
):
    resp_data = generate_response_data()
    mock = mocker.patch("urllib.request.urlopen")
    mock.return_value = request_response(resp_data=resp_data)
    mock.side_effect = URLError("service name")

    url = reverse("sheet-view")

    resp = api_client.get(path=url)

    assert resp.status_code == 404


def test_get_data_404_with_nocache(
        api_client: APIClient,
        mocker: MockerFixture,
        generate_response_data,
        request_response,
        settings,
):
    resp_data = generate_response_data()
    mock = mocker.patch("urllib.request.urlopen")
    mock.return_value = request_response(resp_data=resp_data)
    mock.side_effect = URLError("service name")

    url = reverse("sheet-view") + "?nocache=1"

    resp = api_client.get(path=url)
    assert resp.status_code == 404
