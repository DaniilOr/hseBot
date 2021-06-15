import requests
import json
import bs4 as bs
import io
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Request, Session
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from aiogram.types import InputFile



def get_data():
    resp = requests.get("https://api.binance.com/api/v3/ticker/price")
    return json.loads(resp.text)


def filter_response(resp, N):
    Q_ASSET = "BTC"
    clear_list = []
    for coin in resp:
        if coin["symbol"][-3:] == Q_ASSET:
            clear_list.append({"symbol":coin["symbol"][:-3], "price":coin["price"]})
    return sorted(clear_list, reverse=True, key=lambda x: float(x["price"]))[:N]


def check_name(name):
    all_data = get_data()
    for coin in all_data:
        if coin["symbol"][:-3] == name:
            return True
    return False


def convert(currency1, currency2, sum):
    all_data = get_data()
    if currency1 == currency2:
        return 1.0
    if currency1 == "USDT":
        for coin in all_data:
            if coin["symbol"][-4:] == currency1 and coin["symbol"][:-4] == currency2:
                return sum / float(coin["price"])
    if currency1 in ["BTC", "ETH"]:
        for coin in all_data:
            if coin["symbol"][-3:] == currency1 and coin["symbol"][:-3] == currency2:
                return sum / float(coin["price"])
    else:
        price1 = None
        price2 = None
        print(currency1, currency2)
        if currency2 in ["BTC", "ETH"]:
            print(currency1, currency2)
            for coin in all_data:
                if coin["symbol"][-3:] == currency2 and coin["symbol"][:-3] == currency1:
                    return float(coin["price"]) / sum
        if currency2 == "USD":
            currency2 = currency2 + "T"
            for coin in all_data:
                if coin["symbol"][-4:] == currency2:
                    if coin["symbol"][:-4] == currency1:
                        price1 = coin["price"]
        for coin in all_data:
            if coin["symbol"][-3:] == "BTC":
                if coin["symbol"][:-3] == currency1:
                    price1 = coin["price"]
        for coin in all_data:
            if coin["symbol"][-3:] == "BTC":
                if coin["symbol"][:-3] == currency2:
                    price2 = coin["price"]
        return float(price1) / float(price2) * sum


def parse_news(N):
    url = "https://cryptonews.com/"
    soup = bs.BeautifulSoup(requests.get(url).content, "html.parser")
    articles = soup.find("div", attrs={"class": "cn-list cols"}).find_all("div", attrs={"class": "cn-tile row article"})
    result = []
    for article in articles[:min(N, len(articles))]:
        result.append({"img":article.find("a", attrs={"class":'img'}).find("img")["data-src"],
                       "link":url[:-1]+article.find("a")["href"],
                       "text":article.find("h4").find("a").contents[0]})
    return result


def check_transaction(hash):
    url = f"https://api.etherscan.io/api?module=transaction&action=getstatus&txhash={hash}"
    req = requests.get(url)
    if req.status_code != 200:
        return False
    result = json.loads(req.content)
    return result["result"]["isError"] == '0'


def get_historicalbtc(N):
    start = datetime.now()
    end = start - timedelta(days=N)
    startstr = start.strftime("%Y-%m-%d")
    endstr = end.strftime("%Y-%m-%d")
    url = f"https://api.coindesk.com/v1/bpi/historical/close.json?start={endstr}&end={startstr}"
    req = requests.get(url)
    result = json.loads(req.content)
    delta = timedelta(days=1)
    dates = drange(end, start, delta)
    fig, ax = plt.subplots()
    plt.plot_date(dates, list(result["bpi"].values()))
    plt.plot(dates, list(result["bpi"].values()))
    plt.title(f"Bitcoin growth from {endstr} to {startstr}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid()
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    #plt.show()
    output = io.BytesIO()
    plt.savefig(output)
    output.seek(0)
    return InputFile(path_or_bytesio=output, filename="image.png")
   # b = fig.savefig(fname="image.png")
    #print(b)


if __name__ == "__main__":
    get_historicalbtc(10)
