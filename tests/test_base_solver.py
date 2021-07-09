import unyt as u
from chem_eng_solver.base_solver import Solver
from chem_eng_solver.fluids import FluidsEq


def test__add_units():
    """
    Confirm that method that adds units to numerical answers based on lookup of
    symbol for unknown term works as expected
    """
    solver = Solver(units_out="psi")
    solver.unknown = "P"
    assert solver._add_units(101325, FluidsEq) == 14.6959


def test__convert_units():
    """
    Confirms that method converts units as expected
    """
    solver = Solver()

    # Confirm behavior when input parameter has value == "unknown"
    assert solver.unknown == ""
    assert solver._convert_units("test", "unknown") == "unknown"
    assert solver.unknown == "test"

    # Confirm that method converts units as expected to equivalent SI values
    assert round(solver._convert_units("G", "32.174 ft/s**2"), 2) == 9.81


def test__round_to_sigfigs():
    """
    Confirms that rounding method returns expected number of sigfigs
    """
    solver = Solver()
    assert solver._round_to_sigfigs(1.23456789 * u.ft) == 1.23457
    assert solver._round_to_sigfigs(1.23456789 * u.ft, n=3) == 1.23


def test_find_bounds():
    """
    Confirm that method of finding upper/lower bounds around which an arbitrary
    function crosses zero works as intended
    """
    solver = Solver()

    # Crosses 0 at x = 500, expected bracketing is single crossing (100, 1000)
    func = lambda x: x - 500
    assert solver.find_bounds(func) == [(100, 1000)]
