import pytest
import numpy as np

from chem_eng_solver.stoichiometry import Stoichiometry

TEST_CASES = [
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
    # TODO: Enable parsing of repeat elements such as this example with ethanol
    # {
    #     "input_eq": "CH3CH2OH + O2 --> CO2 + H2O",
    #     "element_balance": {
    #         "C": [2.0, 0.0, -1.0, 0.0],
    #         "H": [6.0, 0.0, 0.0, -2.0],
    #         "O": [0.0, 2.0, -2.0, -1.0],
    #     },
    #     "molecules": {
    #         "reactants": ["CH3CH2OH", "O2"],
    #         "products": ["CO2", "H2O"],
    #     },
    #     "balance": [2.0, 1.0, 2.0],
    #     "result": "CH3CH2OH + 3.5 O2 --> 2.0 CO2 + 3.0 H2O",
    # },
]


def test_stoichiometry_raises_when_no_directional_character_given():
    """
    Confirms that Exception is raised when input_str is missing a ">" character
    """
    with pytest.raises(Exception, match=".*does not contain a '>' character"):
        Stoichiometry("CH4 + O2")


def test_stoichiometry_raises_when_input_eq_is_invalid():
    """
    Not every input_eq value has a valid solution (e.g. user input could be
    wrong). Confirm that when this occurs that appropriate error is raised when
    attepting to find balanced equation.
    """
    with pytest.raises(Exception, match="Could not find balanced equation.*"):
        # Correct form of this input equation is "CaCO3 --> Ca + CO + O2"
        Stoichiometry("CaCO3 --> Ca + CO2")


def test_stoichiometry_raises_when_elements_not_present_on_both_sides_of_eq():
    """
    Confirm that error is thrown if input equation is invalid because any
    element is missing from one side of chemical equation.
    """
    with pytest.raises(Exception, match=".*is not present on both sides.*"):
        Stoichiometry("CaF2 --> Ca")


def test_stoichiometry():
    """
    Confirms that Stoichiometry class works as intended for every defined test
    case
    """
    for case in TEST_CASES:
        st = Stoichiometry(case["input_eq"])
        for name, value in case.items():
            assert getattr(st, name) == value
