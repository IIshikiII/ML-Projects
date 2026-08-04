import timeit
import sys
from functools import reduce


def check_arguments(supported_arguments: list) -> int:
    res = 0
    if len(sys.argv) != 4:
        print("Invalid number of arguments")
        res = 1
    elif sys.argv[1] not in supported_arguments:
        print("Command is not supported")
        res = 2
    elif not sys.argv[2].isdigit():
        print("Invalid number of function calls")
        res = 3
    elif not sys.argv[3].isdigit():
        print("Invalid number for sum of the calculation of squares")
        res = 4

    return res


def call_function(function: str, functions: dict, number: int) -> list:
    res = functions[function](number)
    return res


def sum_loop(number: int) -> int:
    sum = 0
    for i in range(1, number + 1):
        sum = sum + i**2
    return sum


def sum_reduce(number: int) -> int:
    return reduce(lambda x, y: x + y**2, range(1, number+1))


if __name__ == "__main__":
    supported_functions = {
        "loop": sum_loop,
        "reduce": sum_reduce
    }

    if check_arguments(list(supported_functions.keys())) == 0:
        function = sys.argv[1]
        function_calls_number = int(sys.argv[2])
        count_for_sum = int(sys.argv[3])

        res_time = timeit.timeit(
            lambda: call_function(
                function, supported_functions, count_for_sum),
            number=function_calls_number
        )

        print(res_time)
