import pytest
import numpy as np

from chem_eng_solver.stoichiometry import Stoichiometry

TEST_CASES = [
    {
        "test_str": "CH4 + O2 --> CO2 + H2O",
        "elemental_balance": {
            "C": [1.0, 0.0, -1.0, 0.0],
            "H": [4.0, 0.0, 0.0, -2.0],
            "O": [0.0, 2.0, -2.0, -1.0],
        },
    },
]


def test_stoichiometry_raises_when_no_directional_character_given():
    """
    Confirms that Exception is raised when input_str is missing a ">" character
    """
    with pytest.raises(Exception, match=".*does not contain a '>' character"):
        Stoichiometry("CH4 + O2")


def test_stoichiometry():
    """
    Confirms that Stoichiometry class works as intended for every defined test
    case
    """
    for case in TEST_CASES:
        st = Stoichiometry(case["test_str"])
        assert st.input_eq == case["test_str"]
        assert st.element_balance == case["elemental_balance"]
        assert isinstance(st.balance, np.ndarray)
