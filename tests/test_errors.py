"""Test that error messages occur from the files in tests/input."""
import io
from collections import defaultdict
from contextlib import redirect_stdout
from pathlib import Path
from typing import Dict

import pytest
from packaging.specifiers import SpecifierSet, InvalidSpecifier
from pylint import run_pylint

from pylint_nautobot import CHECKERS


def get_error_tests():
    """Get all the tests from tests/input."""
    error_tests = defaultdict(dict)
    good_tests = defaultdict(dict)

    input_folder = Path(__file__).parent / "input"

    for file in input_folder.glob("error_*"):
        error_tests[file.stem][file.suffix.strip(".")] = file

    for file in input_folder.glob("good_*"):
        good_tests[file.stem][file.suffix.strip(".")] = file
    return list(error_tests.values()), list(good_tests.values())


ERROR_TESTS, GOOD_TESTS = get_error_tests()


def test_version_specifiers():
    for checker in CHECKERS:
        try:
            SpecifierSet(checker.version_specifier)
        except InvalidSpecifier:
            pytest.fail(f"Version specifier {checker.version_specifier} doesn't parse.")


@pytest.mark.parametrize("test_file_path", ERROR_TESTS, ids=[test["py"].stem for test in ERROR_TESTS])
def test_errors(test_file_path):
    run_test(test_file_path, error=True)


@pytest.mark.parametrize("test_file_path", GOOD_TESTS, ids=[test["py"].stem for test in GOOD_TESTS])
def test_no_errors(test_file_path):
    run_test(test_file_path, error=False)


def run_test(test_file_path: Dict[str, Path], error: bool):
    """Run a single test."""
    # Extract the checker name from the file name
    checker_name = test_file_path["py"].stem[6:].replace("_", "-")

    # We only have error output for error tests
    if error:
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
                    "--disable=all",
                    f"--enable={checker_name}",
                ]
            )
        except SystemExit as system_exit:
            if system_exit.code == 0 and error:
                pytest.fail(f"Didn't generate error message for check '{checker_name}'.")
            if system_exit.code != 0 and not error:
                pytest.fail(f"Generated error message for check '{checker_name}.")
        actual_output = buf.getvalue()

    # Since we only have an expected output for error tests, only compare if we are
    # running an error test.
    if error:
        for expected_error in expected_output.strip().splitlines():
            assert expected_error in actual_output
