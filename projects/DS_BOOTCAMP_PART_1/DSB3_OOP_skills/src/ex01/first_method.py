"""
Module for reading CSV files.

Classes
-------
Research
    Reads the content of a hardcoded CSV file and returns it as a string.
"""


class Research:
    """
    A class used to read hardcoded file.

    Reads the file located at '../data.csv' and returns its content as text.


    Methods
    -------
    file_reader():
        Read the content of '../data.csv' and return the content of this file as a sole string
    """

    def file_reader(self) -> str:
        """
        Read the content of '../data.csv' and return the content of this file as a sole string.

        Returns
        -------
        str
            Content of '../data.csv' 
        """
        file_path = "../data.csv"
        with open(file_path) as f:
            text = ''.join(f.readlines())
        return text


if __name__ == "__main__":
    print(Research().file_reader())
