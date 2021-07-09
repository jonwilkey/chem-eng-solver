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
]

# Define examples of bad input strings that should raise exceptions listed
BAD_CASES_INITIAL_PARSER = [
    ("123kg/m**3", ".*doesn't match expected parsing pattern.*"),
    ("123E15 kg/m**3", ".*doesn't match expected parsing pattern.*"),
    ("1/4 kg/m**3", ".*doesn't match expected parsing pattern.*"),
]
BAD_CASES_UNITS_PARSER = [
    ("kg/(m**3)", "Cannot determine how to build .* into final_units .*"),
]


def test__initial_parser():
    """
    Confirms that _initial_parser returns expected output for all test cases
    """
    for input_str, expected_output, _, _ in CASES:
        value, units_str = Units._initial_parser(input_str)
        assert isinstance(value, float)
        assert value == expected_output[0]
        assert units_str == expected_output[1]


def test__initial_parser_raises():
    """
    Confirms that _initial_parser raises exception on bad input string
    """
    for input_str, exception_msg in BAD_CASES_INITIAL_PARSER:
        with pytest.raises(Exception, match=exception_msg):
            Units._initial_parser(input_str)


def test__units_parser():
    """
    Confirms that _units_parser returns expected output for all test cases
    """
    for _, _initial_parser_output, expected_output, _ in CASES:
        _, units_str = _initial_parser_output
        units = Units._units_parser(units_str)
        assert units == expected_output


def test__units_parser_raises():
    """
    Confirms that _units_parser raises exception on bad input string
    """
    for input_str, exception_msg in BAD_CASES_UNITS_PARSER:
        with pytest.raises(Exception, match=exception_msg):
            Units._units_parser(input_str)


def test_count_sigfigs():
    """
    Confirms that method for counting sigfigs works as intended
    """
    # Confirm that by default sigfigs starts out as max_sigfigs argument
    units = Units(max_sigfigs=6)
    assert units.sigfigs == 6

    # Confirm that parsing sigfigs counts correctly
    units.count_sigfigs(-0.0001079)
    assert units.sigfigs == 4  # TODO: this is wrong, should be 7

    # Confirms that sigfigs remains at lowest value that is given to method
    units.count_sigfigs(1.0/3.0)
    assert units.sigfigs == 4

    # TODO: need to ensure that when parsing value from str -> float we keep
    # track that this was originally 0.00000 and not 0.0
    # assert units.count_sigfigs("0.00000") == 5


def test_unit_converter():
    """
    Confirms that unit_converter returns expected output for all test cases
    """
    units = Units()
    for input_str, _, _, expected_output in CASES:
        converted_value = units.unit_converter(input_str)
        assert isinstance(converted_value, float)
        assert converted_value == expected_output
        assert units.sigfigs == 3
