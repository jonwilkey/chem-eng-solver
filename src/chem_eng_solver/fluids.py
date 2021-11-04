"""Module for fluid dynamics equations and solvers."""

from types import SimpleNamespace
from typing import Dict

import unyt as u
from scipy.optimize import brentq

from chem_eng_solver.base_solver import UNKNOWN, EqRegistry, Solver

G = float(u.physical_constants.standard_gravity.value)


class FluidsEq(EqRegistry):
    """Defines general form of fluid equations and their nomenclature / units.

    Attributes:
        bernoulli (str): The Bernoulli equation for an incompressible fluid.
    """

    class units(SimpleNamespace):
        """Nomenclature and units for all terms used in equations.

        Attributes:
            h (m): Height
            G (m/s**2): Accelaration due to gravity
            P (Pa): Pressure
            rho (kg/m**3): Density
            v (m/s): Velocity
        """

        h = u.m
        G = u.m / u.s ** 2
        P = u.pascal
        rho = u.kg / u.m ** 3
        v = u.m / u.s

    # Define equations here
    bernoulli = "0.5 * {rho} * {v} ** 2 + {rho} * G * {h} + {P}"


class Fluids(Solver):
    """Class for solving fluid dynamics equations."""

    def __init__(
        self,
        initial: Dict[str, str],
        final: Dict[str, str],
        **kwargs,
    ) -> None:
        """Initialize class.

        Args:
            initial (Dict[str, str]): Initial values for system (v, P, etc.).
            final (Dict[str, str]): Final values for system.
            kwargs: Additional keyword arguments to :cls:`Solver` parent class.
        """
        super().__init__(**kwargs)

        # Parse input arguments and perform unit conversions
        self.initial = {k: self._convert_units(k, v) for k, v in initial.items()}
        self.final = {k: self._convert_units(k, v) for k, v in final.items()}

    def bernoulli(self) -> str:
        """Finds roots to Bernoulli equation.

        Works on the principle of conservation of energy (initial = final --> initial -
        final = 0). Uses `scipy.optimize.brentq` as algorithm for finding all roots.
        Note that multiple solutions to the equation may exist depending on the term
        being solved for (e.g. v is squared, so both + and - roots will exist when
        solving for v_initial or v_final).

        Method saves solution to :attr:`solutions` in SI units as well as returning the
        string representation of solved roots.

        Returns:
            str: String representation of solution in SI units.
        """
        func = eval(
            f"lambda {UNKNOWN}: {FluidsEq.bernoulli.format(**self.initial)} - "
            f"({FluidsEq.bernoulli.format(**self.final)})"
        )
        bounds = self.find_bounds(func)
        solutions = [brentq(func, lwr, upr) for lwr, upr in bounds]
        self.solutions = []
        for root in solutions:
            # NOTE: ignoring mypy because it types FluidsEq.units as Type[units], not
            # SimpleNamespace, which will then cause mypy to fail.
            self.solutions.append(self._add_units(root, FluidsEq.units))  # type: ignore
        return (
            f"{self.unknown} = "
            f"{' or '.join([root.__str__() for root in self.solutions])}"
        )
