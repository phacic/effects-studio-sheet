from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator, List

import pytest
from faker import Faker

fake = Faker()


@pytest.fixture(autouse=True)
def use_temp_base_dir(settings):
    """
    use a tempdir as base dir
    """
    temp_base = TemporaryDirectory()
    settings.BASE_DIR = Path(temp_base.name)
    settings.SAVED_CSV_FILE_PATH = Path.joinpath(
        settings.BASE_DIR, settings.SAVED_CSV_FILE
    )

    yield
    temp_base.cleanup()


@pytest.fixture(scope="session")
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture()
def generate_response_data():
    """
    generate a mock response
    """

    def do_gen(rows=20) -> bytes:
        # add 1 for header
        rows = rows + 1 if rows > 0 else rows

        byte_data = b""
        for i in range(rows):
            if i == 0:
                # header
                byte_data += b"title,description,image\n"
            else:
                line = f"{fake.word()},description {fake.word()},{fake.image_url()}\n"
                byte_data += bytes(line, "utf-8")

        return byte_data

    return do_gen


class MockResponse:
    """
    mock response for urllib.request.open
    """

    def __init__(self, resp_data, code=200, msg="OK"):
        self.resp_data: bytes = resp_data
        self.code = code
        self.msg = msg
        self.headers = {"content-type": "text/csv; charset=utf-8"}

    def read(self):
        return self.resp_data

    def readlines(self):
        lines = list(self.resp_data.split(b"\n"))

        # the last line is sometimes empty
        count = len(lines)
        if not lines[count - 1]:
            lines.pop(count - 1)
        return lines

    def getcode(self):
        return self.code


@pytest.fixture()
def request_response():
    """
    urllib request response
    """

    def do_response(resp_data: bytes, code=200, msg="OK"):
        return MockResponse(resp_data=resp_data, code=code, msg=msg)

    return do_response
