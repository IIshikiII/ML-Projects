def data_types():
    """The function that print 8 basic data types in Python"""
    integer = 7
    string = "str"
    floating = 7.7
    boolean = True
    lst = [1, 2, 3]
    dct = {"key": "value"}
    tpl = (7, 7)
    st = {1, 2, 3, 4}

    print("[", end="")
    print(
        type(integer).__name__, type(string).__name__,
        type(floating).__name__, type(boolean).__name__,
        type(lst).__name__, type(dct).__name__,
        type(tpl).__name__, type(st).__name__,
        end="",
        sep=", "
    )
    print("]\n", end="")


if __name__ == "__main__":
    data_types()
