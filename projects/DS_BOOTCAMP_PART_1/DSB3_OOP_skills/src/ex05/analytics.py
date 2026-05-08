"""
Module for reading CSV files.

Classes
-------
Research
    Reads the file located at '/src' folder and returns it content.
    Contains nested Calculations class for data analysis.
"""
import os
from random import randint


class Research:
    """
    A class used to read a specified file.

    Reads the file located at '/src' folder and returns its content.


    Attributes
    ----------
    file_path : str
        Full path to the file to be processed.
    observations_number : int
        Number of data rows read from the file (excluding header).

    Methods
    -------
    file_reader():
        Read the content of file and return them as a list of lists of ints
    check_file_content(text):
        Validates the format of the file content

    Nested Classes
    --------------
    Calculations
        Class for statistical analysis of the parsed data.
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

    def file_reader(self, has_header: bool = True) -> list[list[int]]:
        """
        Read the content of file and return them as a list of lists of ints.

        Parameters
        ----------
        has_header : bool, default=True
            If the processed file has header line or not

        Returns
        -------
        list[list[int]]
            Parsed content of the file as 2D list of integers

        Raises
        ------
        ValueError
            If the content of the file is not valid

        Side Effects
        ------------
        Sets the `observations_number` attribute to the number of data rows.
        """
        with open(self.file_path) as f:
            text = ''.join(f.readlines())
            self.check_file_content(text, has_header)

        lines = [line.strip()
                 for line in text.strip().split("\n") if line.strip()]
        res = [line.split(',') for line in lines]
        if has_header:
            res = res[1:]  # deleting first element
        res = [list(map(int, line)) for line in res]
        self.observations_number = len(res)
        return res

    def check_file_content(self, text: str, has_header: bool) -> None:
        """
        Validate the format of the file content.

        The file must contain valid CSV data with two columns.
        When has_header=True,
        first line must contain two comma-separated column names.
        Data lines must be either "0,1" or "1,0".

        Parameters
        ----------
        text : str
            The complete file content to validate
        has_header : bool
            Whether to treat the first non-empty line as a header

        Raises
        ------
        ValueError
            If the file content format is invalid
        """
        lines = [line.strip()
                 for line in text.strip().split("\n") if line.strip()]

        if not lines:
            raise ValueError("File is empty")

        if has_header:
            if len(lines[0].split(',')) != 2:
                raise ValueError(
                    "Invalid header format. "
                    "Expected exactly two comma-separated column names"
                )
            data_start = 1  # Skip header line
        else:
            data_start = 0  # Start from first line

        # Check if there's any data after header (if present)
        if data_start >= len(lines):
            raise ValueError("File contains no data")

        # Data validation
        for i, line in enumerate(lines[data_start:], start=data_start + 1):

            if line not in ["0,1", "1,0"]:
                raise ValueError(
                    f"Invalid values at line {i}. "
                    f"Expected '0,1' or '1,0', got: '{line}'"
                )

    class Calculations:
        """
        A class for analysis of the content of the specified file.

        This class is nested  to provide analytical methods
        for processing data read from the file

        Methods
        -------
        counts(content):
            Count the quantity of heads and tails in file.
        fractions(heads, tails):
            Calculate the fractions of heads and tails.
        """

        def __init__(self, content: list[list[int]]) -> None:
            """
            Initialize the data attribute of the class.

            Parameters
            ----------
            content: list[list[int]]
                The content of the processed file
            """
            self.data = content

        def counts(self) -> tuple[int, int]:
            """
            Count the quantity of heads and tails.

            Returns
            -------
            tuple[int, int]
                The calculated quantity of heads and tails
            """
            heads = 0
            tails = 0
            for elem in self.data:
                heads += elem[0]
                tails += elem[1]

            return heads, tails

        def fractions(self, heads: int, tails: int) -> tuple[float, float]:
            """
            Calculate the fractions of heads and tails.

            Parameters
            ----------
            heads : int
                Quantity of heads in file
            tails : int
                Quantity of tails in file

            Returns
            -------
            tuple[float, float]
                The calculated fractions of heads and tails
            """
            heads_ratio = heads / (tails + heads)
            tails_ratio = tails / (tails + heads)
            return heads_ratio, tails_ratio

    class Analytics(Calculations):
        """
        A class for generating random coin flip predictions.

        This class is extends `Calculations' with methods for predictions.

        Methods
        -------
        predict_random(n)
            Generate n predicions
        predict_last()
            Get last item of data from file_reader()
        """

        def predict_random(self, n: int) -> list[list[int]]:
            """
            Return n random coin flips as [head, tail] pairs.

            Parameters
            ----------
            n : int
                Number of predictions

            Returns
            -------
            list[list[int]]
                List of n simulated coin flip outcomes
            """
            res = []
            for _ in range(n):
                head = randint(0, 1)
                tail = 1 - head
                res.append([head, tail])

            return res

        def predict_last(self) -> list[int]:
            """Return the last item of data from file_reader()."""
            return self.data[-1]

        def save_file(self, data_to_file: str,
                      file_name: str, extension: str) -> None:
            """
            Save any given information to file.

            Parameters
            ----------
            data_to_file : str
                Data to save into file.
            file_name : str
                The name of the file.
            extension : str
                _The extention of the file.
            """
            with open(file_name+"."+extension, "w") as f:
                f.write(data_to_file)
