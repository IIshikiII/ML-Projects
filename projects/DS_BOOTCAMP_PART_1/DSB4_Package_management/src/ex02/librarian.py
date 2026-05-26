import os
import subprocess
import sys


class VenvError(Exception):
    """Basic exception for virtual environment errors"""
    pass


class VenvNotActivatedError(VenvError):
    """Raised when the virtual environment is not activated."""
    pass


class WrongVenvError(VenvError):
    """Raised when an invalid virtual environment is activated."""
    pass


def check_env() -> None:
    current_venv = os.environ.get("VIRTUAL_ENV")
    if current_venv is None:
        raise VenvNotActivatedError("Venv is not activated")
    elif os.path.basename(current_venv) != "antoniju":
        raise WrongVenvError("Invalid venv is acivared")


def install(packages: list[str]) -> None:
    subprocess.run([sys.executable, "-m", "pip", "install",
                   *packages], stdout=subprocess.PIPE)


def save_requirements(requirements: str) -> None:
    with open("requirements.txt", "w") as f:
        f.writelines(requirements)


def get_installed_packages() -> str:
    res = subprocess.run([sys.executable, "-m", "pip",
                         "freeze"], stdout=subprocess.PIPE).stdout
    return str(res, 'utf-8')


if __name__ == "__main__":
    check_env()
    packages = ["BeautifulSoup4", "PyTest", "requests"]

    install(packages)
    requirements = get_installed_packages()

    print(requirements)
    save_requirements(requirements)
