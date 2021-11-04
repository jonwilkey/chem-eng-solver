"""Tests for units.py module."""

import pytest
import unyt as u

from chem_eng_solver.units import Units

# Define test cases here, pattern is:
# (
#     input_str,
#     expected _initial_parser output,
#     expected _units_parser output,
#     expected unit_converter output,
# )
CASES = [
    ("123 kg / m^3", (123.0, "kg / m^3"), 1 * u.kg / u.m ** 3, 123.0),
    ("123.0 kg / m^3", (123.0, "kg / m^3"), 1 * u.kg / u.m ** 3, 123.0),
    ("-123 kg / m^3", (-123.0, "kg / m^3"), 1 * u.kg / u.m ** 3, -123.0),
    ("0.123 kg / m^3", (0.123, "kg / m^3"), 1 * u.kg / u.m ** 3, 0.123),
    (".123 kg / m^3", (0.123, "kg / m^3"), 1 * u.kg / u.m ** 3, 0.123),
    ("123 kg*m^-3", (123.0, "kg*m^-3"), 1 * u.kg / u.m ** 3, 123.0),
    ("-123 kg/m^3*m/m", (-123.0, "kg/m^3*m/m"), 1 * u.kg / u.m ** 3, -123.0),
    ("123 /m^3", (123.0, "/m^3"), 1 / u.m ** 3, 123.0),
    ("123E15 kg/m**3", (123e15, "kg/m**3"), 1 * u.kg / u.m ** 3, 123e15),
    ("123e15 kg/m**3", (123e15, "kg/m**3"), 1 * u.kg / u.m ** 3, 123e15),
]

# Define examples of bad input strings that should raise exceptions listed
BAD_CASES_INITIAL_PARSER = [
    ("123kg/m**3", ".*doesn't match expected parsing pattern.*"),
    ("1/4 kg/m**3", ".*doesn't match expected parsing pattern.*"),
]
BAD_CASES_UNITS_PARSER = [
    ("kg/(m**3)", "Cannot determine how to build .* into final_units .*"),
]


def test__initial_parser():
    """Confirms that _initial_parser returns expected output for all test cases."""
    units = Units()
    for input_str, expected_output, _, _ in CASES:
        value, units_str = units._initial_parser(input_str)
        assert isinstance(value, float)
        assert value == expected_output[0]
        assert units_str == expected_output[1]


def test__initial_parser_raises():
    """Confirms that _initial_parser raises exception on bad input string."""
    units = Units()
    for input_str, exception_msg in BAD_CASES_INITIAL_PARSER:
        with pytest.raises(Exception, match=exception_msg):
            units._initial_parser(input_str)


def test__units_parser():
    """Confirms that _units_parser returns expected output for all test cases."""
    for _, _initial_parser_output, expected_output, _ in CASES:
        _, units_str = _initial_parser_output
        units = Units._units_parser(units_str)
        assert units == expected_output


def test__units_parser_raises():
    """Confirms that _units_parser raises exception on bad input string."""
    for input_str, exception_msg in BAD_CASES_UNITS_PARSER:
        with pytest.raises(Exception, match=exception_msg):
            Units._units_parser(input_str)


def test_count_sigfigs():
    """Confirms that method for counting sigfigs works as intended."""
    # Confirm that by default sigfigs starts out as max_sigfigs argument
    units = Units(max_sigfigs=12)
    assert units.sigfigs == 12

    # Confirm that parsing sigfigs counts correctly
    units.count_sigfigs("-0.0001079")
    assert units.sigfigs == 7

    # Confirms that sigfigs remains at lowest value that is given to method
    units.count_sigfigs(str(1.0 / 3.0))
    assert units.sigfigs == 7

    # Even when all zeros counts sig figs correctly
    units.count_sigfigs(".00000")
    assert units.sigfigs == 5

    # Sandwiched zeros count
    units.count_sigfigs("1001")
    assert units.sigfigs == 4

    # Leading zeros ignored
    units.count_sigfigs("001.00")
    assert units.sigfigs == 3

    # Trailing zeros ignored
    units.count_sigfigs("100")
    assert units.sigfigs == 1


def test_unit_converter():
    """Confirms that unit_converter returns expected output for all test cases."""
    units = Units()
    for input_str, _, _, expected_output in CASES:
        converted_value = units.unit_converter(input_str)
        assert isinstance(converted_value, float)
        assert converted_value == expected_output
        assert units.sigfigs == 3
