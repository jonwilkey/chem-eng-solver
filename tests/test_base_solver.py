"""Tests for base_solver.py module."""

import pytest
import unyt as u

from chem_eng_solver.base_solver import EqRegistry, Solver
from chem_eng_solver.fluids import FluidsEq


def test__add_units():
    """Tests :meth:`_add_units`.

    Confirms that method adds units to numerical answers based on lookup of symbol for
    unknown term as expected.
    """
    solver = Solver(units_out="psi")
    solver.unknown = "P"
    assert solver._add_units(101325, FluidsEq.units) == 14.6959


def test__convert_units():
    """Test for :meth:`_convert_units`.

    Confirms that method converts units as expected.
    """
    solver = Solver()

    # Confirm behavior when input parameter has value == "unknown"
    assert solver.unknown == ""
    assert solver._convert_units("test", "unknown") == "unknown"
    assert solver.unknown == "test"

    # Confirm that method converts units as expected to equivalent SI values
    assert round(solver._convert_units("G", "32.174 ft/s**2"), 2) == 9.81


def test__round_to_sigfigs():
    """Test for :meth:`_round_to_sigfigs`.

    Confirms that rounding method returns expected number of sigfigs.
    """
    solver = Solver()
    assert solver._round_to_sigfigs(1.23456789 * u.ft) == 1.23457
    assert solver._round_to_sigfigs(1.23456789 * u.ft, n=3) == 1.23


def test_find_bounds():
    """Test for :meth:`find_bounds`.

    Confirm that method of finding upper/lower bounds around which an arbitrary
    function crosses zero works as intended.
    """
    solver = Solver()

    def simple_function(x: float) -> float:
        """Function that has a root at x = 500.

        Expected bracketing when passed to :meth:`find_bounds` is [100, 1000]

        Args:
            x (float): Independent variable

        Returns:
            float: y-value according to equation y = x - 500.
        """
        return x - 500

    assert solver.find_bounds(simple_function) == [(100, 1000)]


def test_eq_registry_raises_when_abstractmethod_remains():
    """Confirms that :cls:`EqRegistry` can't be instantiated with abstractmethod."""

    class MockClass(EqRegistry):
        pass

    with pytest.raises(TypeError, match="Can't .* with abstract methods units"):
        MockClass()
