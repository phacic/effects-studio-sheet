import csv
import logging
import urllib.request
from http.client import HTTPResponse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.error import URLError

from django.conf import settings

logger = logging.getLogger(__name__)


def fetch_file() -> Tuple[Optional[URLError], Optional[HTTPResponse]]:
    """
    fetch the Google sheet

    Returns:
        either an exception or a response
    """
    if not settings.SHEET_FILE_ID:
        raise ValueError("SHEET_FILE_ID variable has to be set")

    try:
        url = f"https://docs.google.com/spreadsheets/d/{settings.SHEET_FILE_ID}/gviz/tq?tqx=out:csv"
        return None, urllib.request.urlopen(url)
    except URLError as ex:
        logger.exception("could not fetch Google sheet")
        return ex, None


def save_sheet() -> Optional[URLError]:
    """
    save response in csv to access later
    """

    err, resp = fetch_file()
    if err:
        return err

    content = resp.read()
    with open(settings.SAVED_CSV_FILE_PATH, "wb") as csv_file:
        csv_file.write(content)


def read_saved_csv() -> Tuple[Optional[URLError], Optional[List]]:
    """
    read from already saved csv
    """
    csv_file_loc = settings.SAVED_CSV_FILE_PATH

    # check and download the file
    if not Path.exists(csv_file_loc):
        if err := save_sheet():
            return err, None

    with open(csv_file_loc) as csv_file:
        csv_reader = csv.reader(csv_file)
        ls = list(csv_reader)

    return None, ls


def data_to_dict(
    lines: List[List], page: int = None, page_size: int = None
) -> List[Dict]:
    """
    convert list of list to list of dictionary, paginate if requested.
    Args:
        lines: the list to paginate
        page: current page
        page_size: items on a page, defaults to 5
    """
    if not lines:
        return []

    # first lines is the header
    title, descr, image = lines.pop(0)

    # for pagination
    start = 0
    end = len(lines)

    # for pagination range
    if page:
        # default page
        page_size = page_size or 5

        if page == 1:
            end = page_size
        else:
            start = (page - 1) * page_size
            end = page_size * page

    # selection for page
    selected = lines[start:end]
    return [{title: row[0], descr: row[1], image: row[2]} for row in selected]


def load_sheet_data(
    no_cache: bool = True, page: int = None, page_size: int = None
) -> Tuple[Optional[URLError], Optional[List[Dict]]]:
    """
    load data from Google sheet into a list of dict

    Args:
        no_cache: do not save a copy of the sheet (get a fresh one), default to True
        page: pagination page
        page_size: if page size is set the number of items on a page

    Returns:
        List of Dict
    """

    if no_cache:

        # remove saved csv if exist
        Path.unlink(settings.SAVED_CSV_FILE_PATH, missing_ok=True)

        err, resp = fetch_file()
        if err:
            return err, None

        resp_lines = [line.decode() for line in resp.readlines()]
        reader = csv.reader(resp_lines)
        lines = list(reader)
    else:
        err, lines = read_saved_csv()
        if err:
            return err, None

    return None, data_to_dict(lines=lines, page=page, page_size=page_size)
