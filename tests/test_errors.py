"""Test that error messages occur from the files in tests/input."""
import io
from collections import defaultdict
from contextlib import redirect_stdout
from pathlib import Path

import pytest
from pylint import run_pylint


def get_tests():
    """Get all the tests from tests/input."""
    tests = defaultdict(dict)

    input_folder = Path(__file__).parent / "input"

    for file in input_folder.glob("error_*"):
        tests[file.stem][file.suffix.strip(".")] = file
    return list(tests.values())


TESTS = get_tests()


@pytest.mark.parametrize("test_file_path", TESTS, ids=[test["py"].stem for test in TESTS])
def test_errors(test_file_path):
    checker_name = test_file_path["py"].stem.strip("error_").replace("_", "-")
    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            # Runs pylint, disabling all checks except for the one identified by the filename
            run_pylint(
                [
                    str(test_file_path["py"]),
                    "--load-plugins=pylint_nautobot",
                    "--disable=all",
                    f"--enable={checker_name}",
                ]
            )
        except SystemExit as error:
            if error.code == 0:
                pytest.fail(f"Didn't generate error message for check '{test_file_path['py'].stem}'.")
        actual = buf.getvalue()
    with open(test_file_path["txt"], encoding="utf-8") as file:
        expected = file.read()
    assert expected in actual
