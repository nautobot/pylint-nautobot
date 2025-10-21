"""Testing CHECKERS."""

import pytest

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
