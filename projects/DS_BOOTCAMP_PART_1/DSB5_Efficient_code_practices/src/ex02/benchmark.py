import timeit
import sys


def find_mail_cycle(emails: list[str]) -> list:
    res = []
    for mail in emails:
        if mail.endswith("@gmail.com"):
            res.append(mail)
    return res


def find_mail_list_comprehention(emails: list[str]) -> list:
    res = [mail for mail in emails if mail.endswith("@gmail.com")]
    return res


def find_mail_map(emails: list[str]) -> list:
    res = map(lambda mail: mail if mail.endswith(
        "@gmail.com") else None, emails)
    return list(res)


def find_mail_filter(emails: list[str]) -> list:
    res = list(filter(lambda x: x.endswith("@gmail.com"), emails))
    return res


def check_arguments(supported_arguments: list) -> int:
    res = 0
    if len(sys.argv) != 3:
        print("Invalid number of arguments")
        res = 1
    elif sys.argv[1] not in supported_arguments:
        print("Command is not supported")
        res = 2
    elif not sys.argv[2].isdigit():
        print("Invalid number of function calls")
        res = 3

    return res


def call_function(function: str, functions: dict, emails: list) -> list:
    res = functions[function](emails)
    return res


if __name__ == "__main__":
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
              'anna@live.com', 'philipp@gmail.com'] * 5

    supported_functions = {
        'loop': find_mail_cycle,
        'list_comprehension': find_mail_list_comprehention,
        'map': find_mail_map,
        'filter': find_mail_filter
    }
    if check_arguments(list(supported_functions.keys())) == 0:

        function = sys.argv[1]
        function_calls_number = int(sys.argv[2])

        res_time = timeit.timeit(
            lambda: call_function(function, supported_functions, emails),
            number=function_calls_number
        )

        print(res_time)
