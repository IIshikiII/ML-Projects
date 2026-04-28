
import sys


def main() -> None:
    """The main function that encode or decode string with caesar cipher"""
    if check_args() != 0:
        raise Exception("Incorrect number of arguments")

    mode = sys.argv[1]
    text = sys.argv[2]
    shift = int(sys.argv[3])

    if contains_cyrillic(text):
        raise Exception("The script does not support your language yet.")

    if mode == "encode":
        print(encode(text, shift))
    elif mode == "decode":
        print(decode(text, shift))


def check_args() -> int:
    """
    The function that checks arguments
    0 - correct
    1 - incorrect number of arguments
    """
    if len(sys.argv) != 4:
        return 1
    return 0


def contains_cyrillic(text: str) -> bool:
    """The function that check if text contains cyrillic symbols"""
    for char in text:
        if "а" <= char.lower() <= "я" or char == "ё":
            return True
    return False


def encode(text: str, shift: int) -> str:
    """The function that encode text with caesar cipher"""
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        elif char.islower():
            result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
    return result


def decode(text: str, shift: int) -> str:
    """The function that decode text with caesar cipher"""
    return encode(text, -shift)


if __name__ == "__main__":
    main()
