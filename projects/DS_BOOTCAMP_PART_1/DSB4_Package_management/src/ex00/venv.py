import os


def write_env_name():
    print(f"Your current virtual env is {os.environ.get("VIRTUAL_ENV")}")


if __name__ == "__main__":
    write_env_name()
