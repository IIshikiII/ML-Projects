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


if __name__ == "__main__":
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
              'anna@live.com', 'philipp@gmail.com'] * 5

    cycle_time = timeit.timeit(
        lambda: find_mail_cycle(emails=emails), number=90000000)

    list_comprehention_time = timeit.timeit(
        lambda: find_mail_list_comprehention(emails=emails), number=90000000)

    print(
        f"It is better to use {"cycle" if cycle_time < list_comprehention_time else "list comprehention"}")
    print(f"{cycle_time} vs {list_comprehention_time}")
