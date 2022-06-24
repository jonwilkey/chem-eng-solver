"""Tests for units.py module."""

from unittest import TestCase

import unyt as u

from chem_eng_solver.units import Units


class TestUnits(TestCase):
    """Unit tests for the units module."""

    def setUp(self) -> None:
        """Define test fixtures."""
        # Define test cases here, pattern is:
        # (
        #     input_str,
        #     expected _initial_parser output,
        #     expected _units_parser output,
        #     expected unit_converter output,
        # )
        self.cases = [
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
        self.bad_cases_initial_parser = [
            ("123kg/m**3", ".*doesn't match expected parsing pattern.*"),
            ("1/4 kg/m**3", ".*doesn't match expected parsing pattern.*"),
        ]
        self.bad_cases_units_parser = [
            ("kg/(m**3)", "Cannot determine how to build .* into final_units .*"),
        ]

    def test__initial_parser(self):
        """Confirms that _initial_parser returns expected output for all test cases."""
        units = Units()
        for input_str, expected_output, _, _ in self.cases:
            value, units_str = units._initial_parser(input_str)
            self.assertIsInstance(value, float)
            self.assertEqual(value, expected_output[0])
            self.assertEqual(units_str, expected_output[1])

    def test__initial_parser_raises(self):
        """Confirms that _initial_parser raises exception on bad input string."""
        units = Units()
        for input_str, exception_msg in self.bad_cases_initial_parser:
            with self.assertRaisesRegex(Exception, exception_msg):
                units._initial_parser(input_str)

    def test__units_parser(self):
        """Confirms that _units_parser returns expected output for all test cases."""
        for _, _initial_parser_output, expected_output, _ in self.cases:
            _, units_str = _initial_parser_output
            units = Units._units_parser(units_str)
            self.assertEqual(units, expected_output)

    def test__units_parser_raises(self):
        """Confirms that _units_parser raises exception on bad input string."""
        for input_str, exception_msg in self.bad_cases_units_parser:
            with self.assertRaisesRegex(Exception, exception_msg):
                Units._units_parser(input_str)

    def test_count_sigfigs(self):
        """Confirms that method for counting sigfigs works as intended."""
        # Confirm that by default sigfigs starts out as max_sigfigs argument
        units = Units(max_sigfigs=12)
        self.assertEqual(units.sigfigs, 12)

        # Confirm that parsing sigfigs counts correctly
        units.count_sigfigs("-0.0001079")
        self.assertEqual(units.sigfigs, 7)

        # Confirms that sigfigs remains at lowest value that is given to method
        units.count_sigfigs(str(1.0 / 3.0))
        self.assertEqual(units.sigfigs, 7)

        # Even when all zeros counts sig figs correctly
        units.count_sigfigs(".00000")
        self.assertEqual(units.sigfigs, 5)

        # Sandwiched zeros count
        units.count_sigfigs("1001")
        self.assertEqual(units.sigfigs, 4)

        # Leading zeros ignored
        units.count_sigfigs("001.00")
        self.assertEqual(units.sigfigs, 3)

        # Trailing zeros ignored
        units.count_sigfigs("100")
        self.assertEqual(units.sigfigs, 1)

    def test_unit_converter(self):
        """Confirms that unit_converter returns expected output for all test cases."""
        units = Units()
        for input_str, _, _, expected_output in self.cases:
            converted_value = units.unit_converter(input_str)
            self.assertIsInstance(converted_value, float)
            self.assertEqual(converted_value, expected_output)
            self.assertEqual(units.sigfigs, 3)
