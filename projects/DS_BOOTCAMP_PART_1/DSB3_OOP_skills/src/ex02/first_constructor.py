"""
Module for reading CSV files.

Classes
-------
Research
    Reads the file located at '/src' folder and returns it contrent.
"""
import os
import sys


class Research:
    """
    A class used to read a specified file.

    Reads the file located at '/src' folder and returns its content.


    Methods
    -------
    file_reader():
        Read the content of specified file and return them as a sole string
    """

    def __init__(self, filename: str) -> None:
        """
        Initialize one attribute of the object.

        Parameters
        ----------
        filename : str
            Name of file to read and process in other methods
        """
        dirname = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.file_path = os.path.join(dirname, filename)

    def file_reader(self) -> str:
        """
        Read the content of specified file and return them as a sole string.

        Returns
        -------
        str
            Content of content of specified file

        Raises
        ------
        ValueError
            If the contend of the file is not valid
        """
        with open(self.file_path) as f:
            text = ''.join(f.readlines())

        self.check_file_content(text)
        return text

    def check_file_content(self, text: str) -> None:
        """
        Check if the contetnt of file meets requirements.

        Paremeters
        ----------
        text : str
            Content of pecified file

        Raises
        ------
        ValueError
            If the contend of the file is not valid
        """
        lines = text.split("\n")
        if len(lines[0].split(',')) != 2:
            raise ValueError(
                "Incorrect header, "
                "it should be composed of two strings separeted by comma"
            )

        if len(lines) == 1:
            raise ValueError(
                "There is no data in the file"
            )

        for line in lines[1:]:
            if line not in ["0,1", "1,0"]:
                raise ValueError(
                    "Invalid string in the file, "
                    "it shoud be \"0,1\" or \"1,0\""
                )


if __name__ == "__main__":
    file_name = sys.argv[1]
    try:
        print(Research(file_name).file_reader())
    except FileNotFoundError:
        print("This file doesn't exist.")
