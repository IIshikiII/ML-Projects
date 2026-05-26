from urllib.request import Request, urlopen
import ssl
from bs4 import BeautifulSoup
import sys
import time


class RequestError(Exception):
    """Basic exception for request errors"""


def get_page(ticker: str) -> bytes:
    ssl_context = ssl._create_unverified_context()
    req = Request(
        f"https://finance.yahoo.com/quote/{ticker}/financials/")
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('Accept', 'text/html')
    res = urlopen(req, context=ssl_context)
    if res.status == 404:
        raise RequestError("Invalit ticker format")

    return res.read()


def check_ticker(page: BeautifulSoup, field: str) -> None:
    if "Symbols similar to" in str(page) or "My List" in str(page):
        raise RequestError("Ticker does not exist")

    table = page.find(class_="tableBody yf-yuwun0")
    if table is None:
        raise RequestError("Invalid URL, table does not exist on this page")

    field = table.find("div", string=field)  # type: ignore[call-arg]
    if field is None:
        raise RequestError("Field does not exist")


def get_values(soup: BeautifulSoup, field) -> list[str]:
    table = soup.find(class_="tableBody yf-yuwun0")
    field = table.find("div", string=field)  # type: ignore[call-arg]

    row = field.parent.parent  # type: ignore[call-arg]
    value_columns = row.find_all(  # type: ignore[call-arg]
        "div", class_=["column yf-t22klz", "column yf-t22klz alt"])

    return [value.get_text().strip() for value in value_columns]


if __name__ == "__main__":

    ticker = sys.argv[1]
    field = sys.argv[2]

    soup = BeautifulSoup(get_page(ticker), "html.parser")
    check_ticker(soup, field)

    res = (field, *get_values(soup, field))
    print(res)
