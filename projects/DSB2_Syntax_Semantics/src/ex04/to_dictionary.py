def main() -> None:
    """
    The main function thar output exection result
    """
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]
    reversed_countries_dict = reverse_dict(list_of_tuples)
    output(reversed_countries_dict)


def reverse_dict(countries: list[tuple[str, str]]) -> dict[str, set[str]]:
    """Transformation of data into dictionary of sets"""
    countries_dict = dict()
    for country in countries:
        if country[1] not in countries_dict.keys():
            countries_dict[country[1]] = {country[0]}
        else:
            countries_dict[country[1]].add(country[0])

    return countries_dict


def output(countries_dict: dict[str, set[str]]) -> None:
    """Tht function that outputs dictionary in specified format"""
    for number in countries_dict.keys():
        for country in countries_dict[number]:
            print(f"\'{number}\' : \'{country}\'")


if __name__ == "__main__":
    main()
