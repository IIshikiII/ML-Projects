import sys


def main() -> None:
    """
    The main function that 
    1. takes an email address, 
    2. searches for the corresponding name in the file, 
    3. returns the first paragraph of a letter.
    """

    mail = sys.argv[1].strip()
    with open("employees.tsv", "r") as f:
        lines = [line.split("\t")
                 for line in f.readlines()]

    for line in lines:
        if line[2].strip() == mail:
            name = line[0]

    text = f"Dear {name}, welcome to our team! We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires."
    print(text)


if __name__ == "__main__":
    main()
