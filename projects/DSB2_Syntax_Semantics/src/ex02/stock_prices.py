import sys


def main() -> None:
    """
    The main function
    stdin - name of company
    stdout - stock price of company
    """
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    input_data = get_company_name(COMPANIES)

    if input_data[0] == 1:
        pass
    elif input_data[0] == 2:
        pass
    elif input_data[0] == 3:
        print("Unknown company")
    elif input_data[0] == 0:
        search_stock_price(COMPANIES, STOCKS, input_data[1])


def get_company_name(COMPANIES: dict) -> tuple[int, str]:
    """
    The funcion that process input
    0 - correct input
    1 - no input data
    2 - too much arguments
    3 - dictionary of companies does not contain this name
    """
    arguments = sys.argv
    if len(arguments) == 1:
        res = (1, "")
    elif len(arguments) == 2 and arguments[1] in COMPANIES.keys():
        res = (0, arguments[1])
    elif len(arguments) >= 3:
        res = (2, "")
    elif len(arguments) == 2 and arguments[1] not in COMPANIES.keys():
        res = (3, "")
    return res


def search_stock_price(COMPANIES: dict, STOCKS: dict, name: str) -> None:
    print(STOCKS[COMPANIES[name]])


if __name__ == "__main__":
    main()
