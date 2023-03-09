from typing import Callable, List


def assert_not_errors(errors: List) -> None:
    assert not errors, "Errors: %s" % "\n".join(errors)


def valid_object_variable_check(
    valid_entries: List, init_test: Callable, set_test: Callable, get_func: Callable
) -> List:
    errors = []
    for entry in valid_entries:
        # Initialization Test
        try:
            obj = init_test(entry)
        except AssertionError as e:
            errors.append(
                "Valid entry %s was incorrectly rejected with the following message: %s"
                % (entry, e.args[0])
            )
            continue
        var = get_func(obj)
        if var != type(var)(entry):
            errors.append("Valid variable %s was incorrectly set as %s" % (entry, var))
        # Set Test
        try:
            obj = init_test(entry)
            set_test(obj, entry)
        except AssertionError as e:
            errors.append(
                "Valid entry %s was incorrectly rejected with the following message: %s"
                % (entry, e.args[0])
            )
            continue
        var = get_func(obj)
        if var != type(var)(entry):
            errors.append("Valid variable %s was incorrectly set as %s" % (entry, var))
    return errors


def invalid_object_variable_check(
    invalid_entries: List, init_test: Callable, set_test: Callable
) -> List:
    errors = []
    for entry in invalid_entries:
        # Initialization Test
        try:
            obj = init_test(entry)
        except AssertionError:
            pass  # Do nothing, expected
        else:
            errors.append("Invalid variable %s was incorrectly accepted" % (entry))
        # Set Test
        try:
            obj = init_test(entry)
            set_test(obj, entry)
        except AssertionError:
            pass  # Do nothing, expected
        else:
            errors.append("Invalid variable %s was incorrectly accepted" % (entry))
    return errors
