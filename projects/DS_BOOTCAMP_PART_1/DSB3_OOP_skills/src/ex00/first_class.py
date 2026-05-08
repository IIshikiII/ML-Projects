class Must_Read:
    """
    A class used to read and print hardcoded file.

    This class reads the content of '../data.csv' and prints it line by line
    when instantiated.

    Attributes
    ----------
    None
        This class has no instance attributes.

    Methods
    ------- 
    None
        This class has no public methods. The file is read and printed
        during class definition.
    """
    file_path = "../data.csv"
    with open(file_path) as f:
        text = f.readlines()

    print(*text, sep="")


if __name__ == "__main__":
    Must_Read()
