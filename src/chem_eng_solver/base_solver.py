"""This module defines parent equation/solver classes."""

import math
from abc import ABC, abstractmethod
from types import SimpleNamespace
from typing import Callable, List, Optional, Tuple, Union

import numpy as np
import unyt as u

from chem_eng_solver.units import Units

MAX_BOUNDS = 7
UNKNOWN = "unknown"


class EqRegistry(ABC):
    """Defines general form of equations and their nomenclature / units."""

    @abstractmethod
    class units(SimpleNamespace):
        """Nomenclature and units for all terms used in equations.

        Implement in child class as additional named attributes.
        """


class Solver:
    """Class for finding solution to any unknown variable in :class:`EqRegistry`."""

    def __init__(
        self,
        units_out: Optional[str] = None,
    ) -> None:
        """Initialize class.

        Args:
            units_out (Optional[str]): Desired units to return for solution. Defaults to
               `None`, in which case values are reported in SI units.
        """
        self.unit_registry = Units()
        self.units_out = units_out

        # Define initial values
        self.unknown = ""
        self.solutions: List[float] = []

    def _round_to_sigfigs(
        self, x: u.unyt_quantity, n: Optional[int] = None
    ) -> u.unyt_quantity:
        """Rounds input value to sigfigs of :class:`Fluids` input arguments.

        Args:
            x (unyt_quantity): Input value to round to sigfigs.
            n (Optional[int]): Number of sigfigs to round to. Defaults to None, in which
                case the number of sigfigs tracked in `self.unit_registry` is used to
                pick the number of sigfigs.

        Returns:
            unyt_quantity: Input value rounded to specified number of sigfigs.
        """
        n = n if n else self.unit_registry.sigfigs
        value = x.round(-int(math.floor(math.log10(abs(x)))) + (n - 1))
        return value * x.units

    def _convert_units(self, parameter: str, value: str) -> Union[float, str]:
        """Convert input string to value of quantity in SI units.

        If the input matches the :const:`UNKNOWN` string definition, mark the parameter
        as :attr:`self.unknown` (the quantity that will be solved for).

        Args:
            parameter (str): Name of parameter.
            value (str): Quantity of parameter (e.g. "9.81 m/s**2").

        Returns:
            Union[float, str]: Value of quantity in SI units or input string if value
            matches :const:`UNKNOWN` definition.
        """
        if value == UNKNOWN:
            self.unknown = parameter
            return value
        else:
            return self.unit_registry.unit_converter(value)

    def _add_units(
        self, solution: float, eq_registry_units: SimpleNamespace
    ) -> u.unyt_quantity:
        """Applies units to numerical value found in solution method.

        Args:
            solution (float): Numerical value found in solution method (which has SI
                units) for parameter :attr:`self.unknown`.
            eq_registry_units (SimpleNamespace): Object that defines equations used in
                specific module and their units/nomenclature.

        Returns:
            u.unyt_quantity: Solution with units applied (including conversion to
            desired non-SI units if specified in :attr:`self.units_out`).
        """
        quantity = solution * getattr(eq_registry_units, self.unknown)
        quantity = quantity.to(self.units_out) if self.units_out else quantity
        return self._round_to_sigfigs(quantity)

    @staticmethod
    def find_bounds(func: Callable) -> List[Tuple[float, float]]:
        """Finds bounds where :func:`func` has opposite sign.

        Searches over range of values from [-10**:const:`MAX_BOUNDS`,
        10**:const:`MAXBOUNDS`] to support numerical methods that find roots using
        bracketing algorithms like `scipy.optimize.brentq`. Range is evaluated by orders
        of magnitude.

        Args:
            func (Callable): Function to evaluate.

        Returns:
            List[Tuple[float, float]]: Every pair of (x_lwr, x_upr) values for func(x)
            where func had opposite signs over range of values evaluated.
        """
        values = np.array(
            [-(10 ** x) for x in range(MAX_BOUNDS)]
            + [0]
            + [10 ** x for x in range(MAX_BOUNDS)]
        )
        values.sort()
        signs = np.sign(func(values))
        changes: List[Tuple[float, float]] = []
        for idx in range(1, signs[1:].size):
            if signs[idx] != signs[idx - 1]:
                changes.append((values[idx - 1], values[idx]))
        return changes
