"""Tests for fluids.py module."""

from unittest import TestCase

import unyt as u

from chem_eng_solver.fluids import Fluids


class TestFluids(TestCase):
    """Unit tests for the fluids module."""

    def setUp(self) -> None:
        """Define test fixtures."""
        self.initial = {
            "v": "0.0000 ft/s",
            "h": "10.000 yard",
            "P": "14.6959 psi",
            "rho": "998.87 kg/m**3",
        }
        self.final = {
            "v": "unknown",
            "h": "3.00123 m",
            "P": "101325 pascal",
            "rho": "62.423 lb/ft**3",
        }

    def test_bernoulli(self):
        """Confirms that Bernoulli equation solver works as intended."""
        fl = Fluids(self.initial, self.final, units_out="m/s")
        self.assertEqual(fl.bernoulli(), "v = -10.97 m/s or 10.97 m/s")
        self.assertEqual(
            fl.solutions,
            [
                u.unyt_quantity(-10.97, "m/s"),
                u.unyt_quantity(10.97, "m/s"),
            ],
        )
