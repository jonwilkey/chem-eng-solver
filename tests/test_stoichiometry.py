"""Tests for stoichiometry.py module."""

from unittest import TestCase

from chem_eng_solver.stoichiometry import Stoichiometry


class TestStoichiometry(TestCase):
    """Unit tests for the stoichiometry module."""

    def setUp(self) -> None:
        """Define test fixtures."""
        self.test_cases = [
            {
                "input_eq": "CH4 + O2 --> CO2 + H2O",
                "element_balance": {
                    "C": [1.0, 0.0, -1.0, 0.0],
                    "H": [4.0, 0.0, 0.0, -2.0],
                    "O": [0.0, 2.0, -2.0, -1.0],
                },
                "molecules": {
                    "reactants": ["CH4", "O2"],
                    "products": ["CO2", "H2O"],
                },
                "balance": [1.0, 2.0, 1.0, 2.0],
                "result": "CH4 + 2.0 O2 --> CO2 + 2.0 H2O",
            },
            {
                "input_eq": "Na + Cl2 --> NaCl",
                "element_balance": {
                    "Na": [1.0, 0.0, -1.0],
                    "Cl": [0.0, 2.0, -1.0],
                },
                "molecules": {
                    "reactants": ["Na", "Cl2"],
                    "products": ["NaCl"],
                },
                "balance": [2.0, 1.0, 2.0],
                "result": "2.0 Na + Cl2 --> 2.0 NaCl",
            },
            {
                "input_eq": "CH3CH2OH + O2 --> CO2 + H2O",
                "element_balance": {
                    "C": [2.0, 0.0, -1.0, 0.0],
                    "H": [6.0, 0.0, 0.0, -2.0],
                    "O": [1.0, 2.0, -2.0, -1.0],
                },
                "molecules": {
                    "reactants": ["CH3CH2OH", "O2"],
                    "products": ["CO2", "H2O"],
                },
                "balance": [1.0, 3.0, 2.0, 3.0],
                "result": "CH3CH2OH + 3.0 O2 --> 2.0 CO2 + 3.0 H2O",
            },
            {
                "input_eq": "CH3(C(H2))4OH + O2 --> CO2 + H2O",
                "element_balance": {
                    "C": [5.0, 0.0, -1.0, 0.0],
                    "H": [12.0, 0.0, 0.0, -2.0],
                    "O": [1.0, 2.0, -2.0, -1.0],
                },
                "molecules": {
                    "reactants": ["CH3CH2CH2CH2CH2OH", "O2"],
                    "products": ["CO2", "H2O"],
                },
                "balance": [1.0, 7.5, 5.0, 6.0],
                "result": "CH3CH2CH2CH2CH2OH + 7.5 O2 --> 5.0 CO2 + 6.0 H2O",
            },
        ]

    def test_stoichiometry_raises_when_no_directional_character_given(self):
        """Confirm Exception is raised when input_str is missing a ">" character."""
        with self.assertRaisesRegex(Exception, ".*does not contain a '>' character"):
            Stoichiometry("CH4 + O2")

    def test_stoichiometry_raises_when_input_eq_is_invalid(self):
        """Confirm that :cls:`Stoichiometry` raises when input equation is invalid.

        Not every input_eq value has a valid solution (e.g. user input could be
        wrong). Confirm that when this occurs that appropriate error is raised when
        attepting to find balanced equation.
        """
        with self.assertRaisesRegex(Exception, "Could not find balanced equation.*"):
            # Correct form of this input equation is "CaCO3 --> Ca + CO + O2"
            Stoichiometry("CaCO3 --> Ca + CO2")

    def test_stoichiometry_raises_when_elements_not_present_on_both_sides_of_eq(self):
        """Confirm that method raises when element is missing from one side of eq."""
        with self.assertRaisesRegex(Exception, ".*is not present on both sides.*"):
            Stoichiometry("CaF2 --> Ca")

    def test_stoichiometry(self):
        """Confirms that :cls:`Stoichiometry` works as intended for all test cases."""
        for case in self.test_cases:
            st = Stoichiometry(case["input_eq"])
            for name, value in case.items():
                self.assertEqual(getattr(st, name), value)
