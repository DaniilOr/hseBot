import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import io
from typing import Optional


def calculate_min(uid:str, start:Optional=None, end:Optional=None):
    """
        This function calculates min on the range of data. It returns min or None (if there is an error)

        :param uid: str - user id
        :param start: Optional (str or None) - first date to start calculating
        :param end: Optional (str or None) - last date for calculating
    """
    filename = f"files/{uid}.csv"
    if not f"{uid}.csv" in os.listdir("files/"):
        return None
    df = pd.read_csv(filename)
    if start is None and end is None:
        return df["Value"].min()
    df["Date"] = pd.to_datetime(df["Date"])
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    df = df.loc[(df["Date"]>=start) & (df["Date"]<=end)]
    return df["Value"].min()


def calculate_max(uid:str, start:Optional=None, end:Optional=None):
    """
        This function calculates max on the range of data. It returns max or None (if there is an error)

        :param uid: str - user id
        :param start: Optional (str or None) - first date to start calculating
        :param end: Optional (str or None) - last date for calculating
    """
    filename = f"files/{uid}.csv"
    if not f"{uid}.csv" in os.listdir("files/"):
        return None
    df = pd.read_csv(filename)
    if start is None and end is None:
        return df["Value"].max()
    df["Date"] = pd.to_datetime(df["Date"])
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    df = df.loc[(df["Date"]>=start) & (df["Date"]<=end)]
    return df["Value"].max()


def calculate_avg(uid:str, start:Optional=None, end:Optional=None):
    """
        This function calculates mean on the range of data. It returns mean or None (if there is an error)

        :param uid: str - user id
        :param start: Optional (str or None) - first date to start calculating
        :param end: Optional (str or None) - last date for calculating
    """
    filename = f"files/{uid}.csv"
    if not f"{uid}.csv" in os.listdir("files/"):
        return None
    df = pd.read_csv(filename)
    if start is None and end is None:
        return df["Value"].mean()
    df["Date"] = pd.to_datetime(df["Date"])
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    df = df.loc[(df["Date"]>=start) & (df["Date"]<=end)]
    return df["Value"].mean()


def calculate_median(uid:str, start:Optional=None, end:Optional=None):
    """
        This function calculates median on the range of data. It returns median or None (if there is an error)

        :param uid: str - user id
        :param start: Optional (str or None) - first date to start calculating
        :param end: Optional (str or None) - last date for calculating
    """
    filename = f"files/{uid}.csv"
    if not f"{uid}.csv" in os.listdir("files/"):
        return None
    df = pd.read_csv(filename)
    if start is None and end is None:
        return df["Value"].median()
    df["Date"] = pd.to_datetime(df["Date"])
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    df = df.loc[(df["Date"]>=start) & (df["Date"]<=end)]
    return df["Value"].median()


def calculate_std(uid: str, start:Optional=None, end:Optional=None):
    """
        This function calculates std on the range of data. It returns std or None (if there is an error)

        :param uid: str - user id
        :param start: Optional (str or None) - first date to start calculating
        :param end: Optional (str or None) - last date for calculating
    """
    filename = f"files/{uid}.csv"
    if not f"{uid}.csv" in os.listdir("files/"):
        return None
    df = pd.read_csv(filename)
    if start is None and end is None:
        return df["Value"].std()
    df["Date"] = pd.to_datetime(df["Date"])
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    df = df.loc[(df["Date"]>=start) & (df["Date"]<=end)]
    return df["Value"].std()


def plot_dinamics(uid: str, start:Optional=None, end: Optional=None)->Optional:
    """
    This function creates a file with dynamics of prices. It returns None or informs that
    the plot was created

    :param uid: str - user id
    :param start: Optional (str or None) - first date to start plotting
    :param end: Optional (str or None) - last date for plotting
    """
    if f"{uid}.csv" not in os.listdir("files/"):
        return False
    df = pd.read_csv(f"files/{uid}.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    print(df)
    fig, ax = plt.subplots()
    if not start is None and not end is None:
        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")
        df = df.loc[(df["Date"]>=start) & (df["Date"]<=end)]
    plt.plot_date(df["Date"], df["Value"])
    plt.plot(df["Date"], df["Value"])
    plt.title(f"Exchange dynamics")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.grid()
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.savefig(f'files/{uid}.png', dpi = 300)
    return True