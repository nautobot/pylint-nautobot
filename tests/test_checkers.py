"""Testing CHECKERS."""

import pytest
from pylint.lint import PyLinter

from pylint_nautobot import CHECKERS


class TestCheckers:
    """Tests for all checkers."""

    def test_no_duplicate_error_codes(self):
        """Verify that all error codes and message names across all checkers are unique."""
        test_failures = set()
        existing_error_codes = []
        existing_message_names = []

        for checker_class in CHECKERS:
            if hasattr(checker_class, "msgs") and checker_class.msgs:
                for error_code, (_, message_name, _) in checker_class.msgs.items():
                    if error_code in existing_error_codes:
                        test_failures.add(f"Duplicate error code: {error_code}")
                    else:
                        existing_error_codes.append(error_code)
                    if message_name in existing_message_names:
                        test_failures.add(f"Duplicate message name: {message_name}")
                    else:
                        existing_message_names.append(message_name)

        if test_failures:
            pytest.fail(", ".join(sorted(test_failures)))

    def test_no_messages_disabled_by_default(self):
        """Verify that no checker ships a message that is off by default.

        An off-by-default message is effectively invisible, since it is only reachable by someone who already
        knows to look for it. A project that a given check does not apply to is expected to disable it
        explicitly, so that the suppression is a record of intent that can be removed later.
        """
        linter = PyLinter()
        disabled = set()

        for checker_class in CHECKERS:
            linter.register_checker(checker_class(linter))
            for _, message_name, *_ in checker_class.msgs.values():
                if not linter.is_message_enabled(message_name):
                    disabled.add(message_name)

        if disabled:
            pytest.fail(f"Messages disabled by default: {', '.join(sorted(disabled))}")
