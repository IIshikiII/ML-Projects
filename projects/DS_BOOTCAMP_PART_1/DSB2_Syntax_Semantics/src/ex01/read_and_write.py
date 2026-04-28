def read_file(file_name: str) -> list:
    """The function that read file into list of lines"""
    with open(file_name, "r") as f:
        file = f.readlines()
    return file


def process_line(line: str) -> str:
    """The function that replace commats into tabulations"""
    splited_line = line.split("\",")
    splited_data = splited_line[:-1]
    joined_data = "\"\t".join(splited_data) + "\"\t" +\
        splited_line[-1].replace(",", "\t")
    return joined_data


def process_file(file_name: str) -> None:
    """The function that conver csv into tsv"""
    lines = read_file("ds.csv")
    processed_lines = []
    for line in lines:
        processed_lines.append(process_line(line))
    new_file_data = "".join(processed_lines)
    with open("ds.tsv", "w") as f:
        f.write(new_file_data)


if __name__ == "__main__":
    process_file("ds.csv")
