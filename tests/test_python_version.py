import platform
import sys


def test_correct_python():
    python_version = platform.python_version()
    min_version = (3, 10, 0)
    max_version = (3, 10, 13)
    assert (
        min_version <= sys.version_info <= max_version
    ), f"Unsupported Python version: {python_version}"


if __name__ == "__main__":
    test_correct_python()
