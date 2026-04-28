import sys


def main() -> None:
    """The main function that reads file and extract name and surname form email"""

    file_path = sys.argv[1].strip()
    with open(file_path, "r") as f:
        file = f.readlines()
        mails = [mail.replace("\n", "") for mail in file]

    extracted_values = extract_name_surmane(mails)
    with open("employees.tsv", "w") as f:
        f.write("Name\tSurname\tE-mail\n")
        for line in extracted_values:
            f.write(line + "\n")


def extract_name_surmane(mails: list) -> list:
    """The function that extracts names and surnames from list of mails"""
    res = []
    for mail in mails:
        splited_mail = mail.split(".")
        name = splited_mail[0].capitalize()
        surmame = splited_mail[1].split("@")[0].capitalize()
        string = name + "\t" + surmame + "\t" + mail
        res.append(string)
    return res


if __name__ == "__main__":
    main()
