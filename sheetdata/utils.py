import csv
from http.client import HTTPResponse
from pathlib import Path
from typing import Dict, List, Union
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from django.conf import settings

# save csv file location
FILE_LOC = Path.joinpath(settings.BASE_DIR, "data.csv")


def fetch_file() -> Union[Exception, HTTPResponse]:
    """
    fetch the Google sheet

    Returns:
        either an exception or a response
    """
    if not settings.SHEET_FILE_ID:
        raise ValueError("SHEET_FILE_ID variable has to be set")

    try:
        url = f"https://docs.google.com/spreadsheets/d/{settings.SHEET_FILE_ID}/gviz/tq?tqx=out:csv"
        return urlopen(url)
    except Exception in [HTTPError, URLError] as ex:
        return ex


def save_sheet() -> None:
    """
    save response in csv to access later
    """
    resp = fetch_file()
    content = resp.read()
    with open(FILE_LOC, 'wb') as csv_file:
        csv_file.write(content)


def read_saved_csv() -> csv.reader:
    """
    read from already saved csv
    """
    # check and download the file
    if not Path.exists(FILE_LOC):
        save_sheet()

    with open(FILE_LOC) as csv_file:
        csv_reader = csv.reader(csv_file)
        ls = list(csv_reader)

    return ls


def data_to_dict(lines: List[List]) -> List[Dict]:
    """
    convert list of list to list of dictionary
    Args:
         lines
    """

    # first lines is the titles
    title, descr, image = lines.pop(0)
    return [{title: row[0], descr: row[1], image: row[2]} for row in lines]


def load_sheet_data(no_cache: bool, page: int = None, page_size: int = None) -> List[Dict]:
    """
    load data from Google sheet into a list of dict

    Args:
        no_cache: do not save a copy of the sheet (get a fresh one)
        page: pagination page
        page_size: if page size is set the number of items on a page

    Returns:
        List of Dict
    """

    if no_cache:
        # remove saved csv if exist
        Path.unlink(FILE_LOC, missing_ok=True)

        resp = fetch_file()
        resp_lines = [line.decode() for line in resp.readlines()]
        reader = csv.reader(resp_lines)
        lines = list(reader)
    else:
        lines = read_saved_csv()

    return data_to_dict(lines)
