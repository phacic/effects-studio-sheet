import pathlib
from unittest import mock
from django.conf import settings

from sheetdata.utils import load_sheet_data


def test_load_sheet_data(generate_response_data, request_response):
    resp_data = generate_response_data(20)
    with mock.patch("urllib.request.urlopen") as mockr:
        mockr.return_value = request_response(resp_data=resp_data)
        err, data = load_sheet_data(no_cache=False)

        assert not err
        assert len(data) == 20


def test_load_sheet_with_pagination(generate_response_data, request_response):
    resp_data = generate_response_data(20)
    with mock.patch("urllib.request.urlopen") as mockr:
        mockr.return_value = request_response(resp_data=resp_data)
        err, data = load_sheet_data(no_cache=False, page=2, page_size=15)

        assert not err
        assert len(data) == 5


def test_load_sheet_no_cache(generate_response_data, request_response, settings):
    resp_data = generate_response_data(20)
    with mock.patch("urllib.request.urlopen") as mockr:
        mockr.return_value = request_response(resp_data=resp_data)
        err, data = load_sheet_data(no_cache=True)

        assert not err

        # file should not exist
        path = pathlib.Path.joinpath(settings.SAVED_CSV_FILE_PATH)
        assert not path.exists()
