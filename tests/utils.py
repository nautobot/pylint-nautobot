"""Test utilities."""
import astroid
from pylint.testutils import MessageTest


def assert_no_message(test_case, test_code):
    """Assert that no message is emitted for the given code."""
    module_node = astroid.parse(test_code)
    with test_case.assertNoMessages():
        test_case.walk(module_node)


def assert_import_error(test_case, msg_id, test_code, expected_args=None):
    """Assert that the given message is emitted for the given code."""
    module_node = astroid.parse(test_code)
    import_node = module_node.body[0]  # type: ignore
    with test_case.assertAddsMessages(
        MessageTest(
            msg_id=msg_id,
            node=import_node,
            line=1,
            end_line=1,
            col_offset=0,
            end_col_offset=len(test_code),
            args=expected_args,
        ),
    ):
        test_case.walk(module_node)
