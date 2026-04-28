def main() -> None:
    """
    The main function thar output exection result
    """
    countries = {
        '25': {'Russia', 'Brazil'},
        '132': {'France', 'Germany'},
        '178': {'Spain'},
        '162': {'Italy'},
        '17': {'Portugal'},
        '3': {'Finland'},
        '2': {'Hungary'},
        '28': {'The Netherlands', 'Canada'},
        '610': {'The USA'},
        '95': {'The United Kingdom'},
        '83': {'China'},
        '76': {'Iran'},
        '65': {'Turkey'},
        '34': {'Belgium'},
        '26': {'Switzerland'},
        '14': {'Austria'},
        '12': {'Israel'}
    }

    output(countries)


def output(countries: dict) -> None:
    """The function that output countires in ascendling order by number and alphbetic order"""
    keys = sorted(map(int, list(countries.keys())), reverse=True)

    for key in keys:
        countiries_by_id = sorted(countries[str(key)], reverse=True)
        for country in countiries_by_id:
            print(country)


if __name__ == "__main__":
    main()
