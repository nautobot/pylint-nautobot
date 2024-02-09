"""Test utilities."""

from pathlib import Path

import astroid
from pylint.testutils import MessageTest
from pytest import mark

from pylint_nautobot.utils import is_version_compatible


def parametrize_good_files(module):
    path = Path(module)
    checker_name = path.stem[5:].replace("_", "-")
    return mark.parametrize("path", (path.parent / "inputs" / checker_name).glob("good_*.py"))


def parametrize_error_files(module, expected_errors):
    path = Path(module)
    checker_name = path.stem[5:].replace("_", "-")
    inputs_path = path.parent / "inputs" / checker_name
    names = set(item.stem[6:] for item in (inputs_path).glob("error_*.py")) | set(expected_errors)

    def get_params():
        for name in names:
            expected_error = {**expected_errors[name]}
            version = expected_error.pop("version", "")
            if is_version_compatible(version):
                path = inputs_path / f"error_{name}.py"
                yield path, expected_error

    return mark.parametrize(("path", "expected_error"), get_params())


def assert_no_message(test_case, test_code):
    """Assert that no message is emitted for the given code."""
    module_node = astroid.parse(test_code)
    with test_case.assertNoMessages():
        test_case.walk(module_node)


def assert_good_file(test_case, path):
    """Assert that no message is emitted for the given file."""
    assert_no_message(test_case, path.read_text(encoding="utf-8"))


def assert_error_file(test_case, path, expected_error):
    """Assert that the given messages are emitted for the given file.

    Args:
        test_case (unittest.TestCase): The test case instance.
        path (pathlib.Path): The path to the file to test.
        expected_errors (dict): A dictionary of expected errors.
            The keys are part of the filename stripped from prefixed `error_` and `.py`
            e.g. `error_status_model.py` becomes `status_model` key in the dictionary.

    """
    test_code = path.read_text(encoding="utf-8")
    module_node = astroid.parse(test_code)
    node = expected_error.pop("node")
    with test_case.assertAddsMessages(
        MessageTest(
            node=node(module_node),
            **expected_error,
        ),
    ):
        test_case.walk(module_node)


def assert_import_error(test_case, msg_id, test_code, expected_error=None):
    """Assert that the given message is emitted for the given code."""
    module_node = astroid.parse(test_code)
    import_node = module_node.body[0]  # type: ignore
    with test_case.assertAddsMessages(
        MessageTest(
            msg_id=msg_id,
            node=import_node,
            line=1,
            col_offset=0,
            args=expected_error,
        ),
    ):
        test_case.walk(module_node)
