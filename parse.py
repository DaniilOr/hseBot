import json
import pandas as pd
from dateutil.parser import parse
from io import BytesIO
from typing import Optional, Dict

def is_date(string):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    """
    try:
        parse(string, fuzzy=False)
        return True
    except ValueError:
        return False


def validatejson(json_data: Dict) -> bool:
    """
    Validates the inputed json file

    :param json_data: Dict, json, represented as a dictionary
    """
    for item in json_data["dataset"]["data"]:
        if not len(item) == 2:
            return False
        if not is_date(item[0]) or type(item[1]) != float:
            return False
    return True


def json_to_csv(document: bytes, uid: str) -> Optional:
    """
    Saves json as a csv file (from bytes). Returns dataframe or None if something failed

    :param bytes: bytes, contents of file
    :param uid: str, user id
    """
    document = document.decode('utf8').replace("'", '"')
    data = json.loads(document)
    if not validatejson(data):
            return None
    dates = [i[0] for i in data["dataset"]["data"]]
    values = [i[1] for i in data["dataset"]["data"]]
    for v in values:
        if not type(v) == float:
            return None
    df = pd.DataFrame({"Date": dates, "Value": values})
    df.to_csv(f"files/{uid}.csv", index=False)
    return df


def save_csv(bytes : bytes, uid: str) -> Optional:
    """
    Saves a file (from bytes) as csv. Returns dataframe or None if something failed

    :param bytes: bytes, contents of file
    :param uid: str, user id
    """
    bio = BytesIO()
    bio.write(bytes)
    bio.seek(0)
    df = pd.read_csv(bio)

    if not df.columns[0] == "Date" or not df.columns[1] == "Value":
        return None
    for d in df["Date"]:
        if not is_date(d):
            return None
    print("dates checked")
    for v in df["Value"]:
        if not type(v) == float:
            return None
    with open(f"files/{uid}.csv", "wb") as f:
        f.write(bytes)
    return df