from typing import List, Dict
import urllib.request
import csv

import pandas as pd
from django.conf import settings


def load_sheet_data() -> List[Dict]:
    """
    load data from Google sheet into a list of dict
    :return: List of Dict
    """
    if not settings.SHEET_FILE_ID:
        raise ValueError("SHEET_FILE_ID variable has to be set")

    url = f"https://docs.google.com/spreadsheets/d/{settings.SHEET_FILE_ID}/gviz/tq?tqx=out:csv"

    # df = pd.read_csv(url)
    # d = df.to_dict()

    # print(d)

    resp = urllib.request.urlopen(url)
    lines = [line.decode() for line in resp.readlines()]
    reader = csv.reader(lines)
    for row in reader:
        print(row)


