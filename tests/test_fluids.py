"""Tests for fluids.py module."""

import unyt as u

from chem_eng_solver.fluids import Fluids

INITIAL = {
    "v": "0.0000 ft/s",
    "h": "10.000 yard",
    "P": "14.6959 psi",
    "rho": "998.87 kg/m**3",
}
FINAL = {
    "v": "unknown",
    "h": "3.00123 m",
    "P": "101325 pascal",
    "rho": "62.423 lb/ft**3",
}


def test_bernoulli():
    """Confirms that Bernoulli equation solver works as intended."""
    fl = Fluids(INITIAL, FINAL, units_out="m/s")
    assert fl.bernoulli() == "v = -10.97 m/s or 10.97 m/s"
    assert fl.solutions == [
        u.unyt_quantity(-10.97, "m/s"),
        u.unyt_quantity(10.97, "m/s"),
    ]
