import requests
from bs4 import BeautifulSoup
import sys
import time
import pytest


class RequestError(Exception):
    """Basic exception for request errors"""


def get_page(ticker: str) -> bytes:
    headers = {'User-Agent': "Mozilla/5.0", "Accept": "text/html"}
    res = requests.get(
        f"https://finance.yahoo.com/quote/{ticker}/financials/",
        headers=headers
    )
    time.sleep(5)
    if res.status_code == 404:
        raise RequestError("Invalit ticker format")

    return res.content


def check_ticker(page: BeautifulSoup, field: str) -> None:
    if "Symbols similar to" in str(page) or "My List" in str(page):
        raise RequestError("Ticker does not exist")

    table = page.find(class_="tableBody yf-yuwun0")
    if table is None:
        raise RequestError("Invalid URL, table does not exist on this page")

    field = table.find("div", string=field)  # type: ignore[call-arg]
    if field is None:
        raise RequestError("Field does not exist")


def get_values(soup: BeautifulSoup, field) -> tuple:
    table = soup.find(class_="tableBody yf-yuwun0")
    field = table.find("div", string=field)  # type: ignore[call-arg]

    row = field.parent.parent  # type: ignore[call-arg]
    value_columns = row.find_all(  # type: ignore[call-arg]
        "div", class_=["column yf-t22klz", "column yf-t22klz alt"])

    return tuple([value.get_text().strip() for value in value_columns])


if __name__ == "__main__":

    ticker = sys.argv[1]
    field = sys.argv[2]

    soup = BeautifulSoup(get_page(ticker), "html.parser")
    check_ticker(soup, field)

    res = (field, *get_values(soup, field))
    print(res)

# tests


def test_get_page1():
    assert type(get_page("msft")) == bytes


def test_get_page2():
    with pytest.raises(RequestError):
        get_page("????")


def test_get_page3():
    assert type(BeautifulSoup(get_page("appl"),
                "html.parser")) == BeautifulSoup


def test_check_ticker1():
    assert check_ticker(
        BeautifulSoup(
            get_page("msft"),
            "html.parser"
        ),
        "Total Revenue"
    ) is None


def test_check_ticker2():
    with pytest.raises(RequestError):
        check_ticker(
            BeautifulSoup(
                get_page("msft1"),
                "html.parser"
            ),
            "Total Revenue"
        )


def test_check_ticker3():
    with pytest.raises(RequestError):
        check_ticker(
            BeautifulSoup(
                get_page("msft"),
                "html.parser"
            ),
            "Total Revenue1"
        )


def test_get_values1():
    assert type(get_values(
        BeautifulSoup(
            get_page("msft"),
            "html.parser"
        ),
        "Total Revenue"
    )) is tuple


def test_get_values2():
    assert len(get_values(
        BeautifulSoup(
            get_page("msft"),
            "html.parser"
        ),
        "Total Revenue"
    )) == 5


def test_get_values3():
    assert type(get_values(
        BeautifulSoup(
            get_page("nvda"),
            "html.parser"
        ),
        "Total Revenue"
    )[0]) is str
