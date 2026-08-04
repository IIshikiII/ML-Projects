import timeit


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


if __name__ == "__main__":
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
              'anna@live.com', 'philipp@gmail.com'] * 5

    cycle_time = timeit.timeit(
        lambda: find_mail_cycle(emails=emails), number=90000000)

    list_comprehention_time = timeit.timeit(
        lambda: find_mail_list_comprehention(emails=emails), number=90000000)

    map_time = timeit.timeit(
        lambda: find_mail_map(emails=emails), number=90000000
    )

    times = {
        "cycle": cycle_time,
        "list comprehention": list_comprehention_time,
        "map": map_time
    }

    times_items = list(times.items())
    best = min(times_items, key=lambda x: x[1])
    print(f"It is better to use {best}")
    sorted_times = sorted(times.values())
    print(f"{sorted_times[0]} vs {sorted_times[1]} vs {sorted_times[2]}")
