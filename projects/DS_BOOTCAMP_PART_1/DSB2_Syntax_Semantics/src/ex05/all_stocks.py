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

    if check_agrs(COMPANIES) == 0 and check_comma_separeted_str(COMPANIES, STOCKS) == 0:
        arguments = sys.argv[1].split(",")
        for argument in arguments:
            stripped_arg = argument.strip()
            if stripped_arg.upper() in COMPANIES.values():  # if the argument is ticker
                name = search_stock_name(COMPANIES, stripped_arg)
                print(f"{stripped_arg} is a ticker symbol for {name}")
            elif stripped_arg.capitalize() in COMPANIES.keys():  # if the argument is name of company
                ticker = COMPANIES[stripped_arg.capitalize()]
                print(
                    f"{stripped_arg.capitalize()} stock price is {STOCKS[ticker]}")
            else:
                print(
                    f"{stripped_arg} is an unknown company or an unknown ticker symbol")


def check_agrs(COMPANIES: dict) -> int:
    """
    The function that checks arguments
    1 - no arguments
    2 - more than one argument
    0 - OK, one orgument
    """

    arguments = sys.argv
    if len(arguments) == 1:
        res = 1
    elif len(arguments) >= 3:
        res = 2
    else:
        res = 0

    return res


def check_comma_separeted_str(COMPANIES: dict, STOCKS: dict) -> int:
    """
    The function that checks the first argument
    1 - the company name - null-string
    2 - too manny companies in one arguemnt
    0 - OK, one argument
    """
    res = 0
    arguments = sys.argv[1].split(",")
    for argument in arguments:
        stripped_arg = argument.strip()
        if not stripped_arg:
            res = 1
        elif len(stripped_arg.split()) >= 2:
            res = 2

    return res


def search_stock_name(COMPANIES: dict, ticker: str) -> str:
    for key in COMPANIES.keys():
        if COMPANIES[key] == ticker:
            name = key
    return name


if __name__ == "__main__":
    main()
