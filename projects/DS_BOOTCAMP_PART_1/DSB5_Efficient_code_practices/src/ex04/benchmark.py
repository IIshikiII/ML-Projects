import timeit
import random
from collections import Counter


def generare_dictionary(numbers: list[int]) -> dict[int, int]:
    count_dict = dict()
    for number in numbers:
        if number not in count_dict.keys():
            count_dict[number] = 1
        else:
            count_dict[number] += 1
    return count_dict


def top_dictionay(numbers: list[int]) -> list[int]:
    list_numbers = generare_dictionary(numbers).items()
    top_numbers = sorted(list_numbers, key=lambda x: x[1], reverse=True)
    return [number[0] for number in top_numbers][:10]


def generate_dictionary_counter(numbers: list[int]) -> dict[int, int]:
    nums_counter = Counter(numbers)
    res = dict(nums_counter)
    return res


def top_dictionary_counter(numbers: list[int]) -> list[int]:
    nums_counter = Counter(numbers)
    top_values = nums_counter.most_common(10)
    return [elem[0] for elem in top_values]


if __name__ == "__main__":
    random_numbers = [random.randint(1, 100) for _ in range(1000000)]

    my_function_time = timeit.timeit(
        lambda: generare_dictionary(random_numbers),
        number=90
    )

    print("my function:", my_function_time)

    Counter_function_time = timeit.timeit(
        lambda: generate_dictionary_counter(random_numbers),
        number=90
    )
    print("Counter:", Counter_function_time)

    my_top_time = timeit.timeit(
        lambda: top_dictionay(random_numbers),
        number=90
    )
    print("my top:", my_top_time)

    counter_top_time = timeit.timeit(
        lambda: top_dictionary_counter(random_numbers),
        number=90
    )
    print("Counter:", counter_top_time)
