"""Test that error messages occur from the files in tests/input."""
import io
from collections import defaultdict
from contextlib import redirect_stdout
from pathlib import Path

import pytest
from packaging.specifiers import SpecifierSet, InvalidSpecifier
from pylint import run_pylint

from pylint_nautobot import CHECKERS


def get_tests():
    """Get all the tests from tests/input."""
    tests = defaultdict(dict)

    input_folder = Path(__file__).parent / "input"

    for file in input_folder.glob("error_*"):
        tests[file.stem][file.suffix.strip(".")] = file
    return list(tests.values())


TESTS = get_tests()


def test_version_specifiers():
    for checker in CHECKERS:
        try:
            SpecifierSet(checker.version_specifier)
        except InvalidSpecifier:
            pytest.fail(f"Version specifier {checker.version_specifier} doesn't parse.")


@pytest.mark.parametrize("test_file_path", TESTS, ids=[test["py"].stem for test in TESTS])
def test_errors(test_file_path):
    # Extract the checker name from the file name
    checker_name = test_file_path["py"].stem.strip("error_").replace("_", "-")

    with open(test_file_path["txt"], encoding="utf-8") as file:
        expected_output = file.read()

    # Capture stdout to then compare with the .txt test file
    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            # Runs pylint, disabling all checks except for the one identified by the filename
            run_pylint(
                [
                    str(test_file_path["py"]),
                    "--load-plugins=pylint_nautobot",
                    # "--disable=all",
                    # f"--enable={checker_name}",
                ]
            )
        except SystemExit as error:
            if error.code == 0:
                pytest.fail(f"Didn't generate error message for check '{checker_name}'.")
        actual_output = buf.getvalue()
    assert expected_output in actual_output
