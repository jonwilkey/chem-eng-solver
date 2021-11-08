"""Module for solving stoichiometry problems."""

import re
from typing import Dict, List

import numpy as np
from scipy.optimize import lsq_linear

REGEX = {
    "molecules": re.compile("([A-Za-z0-9]+)"),
    "elements": re.compile("([A-Z][a-z]?)([0-9]*)"),
    "groups": re.compile(r"\((.*)\)([0-9]*)"),
}
ROUND_TO_NTH_DECIMAL = 2
SOLUTION_TOLERANCE = 1e-16


class Stoichiometry:
    """Provides methods for balancing chemical equations."""

    def __init__(self, input_eq: str) -> None:
        """Parse input equation to find stoichiometrically balanced version.

        Args:
            input_eq (str): Input equation, e.g. "CH4 + O2 --> CO2 + H2O". Input does
                not need to be balanced (in fact input coefficients are ignored). Must
                contain a ">" character, which is used to identify reactants vs.
                products.

        Raises:
            Exception: if input_str does not contain a ">" character.
        """
        # Confirm that input equation can be parsed into reactants/products
        if ">" not in input_eq:
            raise Exception(
                f"The input:\n\n{input_eq}\n\ndoes not contain a '>' character"
            )
        self.input_eq = input_eq
        input_eq = self._unpack_input_eq_groups(input_eq)

        # This attribute is used to track which side of eq is being operated
        # on in :meth:`_get_element_coeff_matrix` and :meth:`_format_side`
        self._eq_side_is_product = False

        # Create initial element balance
        self.element_balance: Dict[str, List[float]] = {
            element: [] for element, _ in REGEX["elements"].findall(input_eq)
        }

        # Split equation into reactants and products and find molecules in each
        reactants, products = [
            REGEX["molecules"].findall(side) for side in input_eq.split(">")
        ]
        self.molecules = {"reactants": reactants, "products": products}

        # Fill in element balance and validate that every element on reactant
        # side is also present on product side
        for side in (reactants, products):
            self._get_element_coeff_matrix(side)
        self._validate_elemental_balance()

        # Balance equation
        self.balance = self.balance_equation()

        # Format and print result
        self.result = " --> ".join(
            [self._format_result(side) for side in (reactants, products)]
        )
        print(self.result)

    def _unpack_input_eq_groups(self, input_str: str) -> str:
        """Unpacks groups of elements/molecules in :arg:`input_eq`.

        For example, CH3(CH2)2OH would become CH3CH2CH2OH.

        Args:
            input_eq (str): Input string to search for groups to unpack.

        Returns:
            str: Unpacked version of input string.
        """
        groups = REGEX["groups"].findall(input_str)
        for elements, count in groups:
            elements = self._unpack_input_eq_groups(elements)
            multiplier = 1 if count == "" else int(count)
            input_str = REGEX["groups"].sub(elements * multiplier, input_str)
        return input_str

    def _get_element_coeff_matrix(self, eq_side: List[str]) -> None:
        """Parses input equation to find each element and their count in all molecules.

        Results are used to update `self.element_balance` accordingly.

        Args:
            eq_side (List[str]): Molecules on reactant/product side of chemical balance.
                Assumed that this method is called by :meth:`__init__` twice in reactant
                product order, and that :attr:`self._eq_side_is_product` tracks which
                side is being processed.
        """
        for molecule in eq_side:
            composition: Dict[str, float] = {}
            for k, v in REGEX["elements"].findall(molecule):
                count = 1.0 if v == "" else float(v)
                if composition.get(k):
                    composition[k] += count
                else:
                    composition[k] = count
            for element in self.element_balance.keys():
                count = composition.get(element, 0.0)
                if self._eq_side_is_product:
                    count *= -1.0
                self.element_balance[element].append(count)
        self._eq_side_is_product = not self._eq_side_is_product

    def _validate_elemental_balance(self) -> None:
        """Validates that every element found is present on both sides of equation.

        Checks :attr:`self.input_eq` by looking for positive and negative values for
        each element in :attr:`self.element_balance`.

        Raises:
            Exception: If any element isn't present on both sides of equation.
        """
        for element, values in self.element_balance.items():
            n_reactant, n_product = 0, 0
            for value in values:
                if value > 0:
                    n_reactant += 1
                elif value < 0:
                    n_product += 1
            if n_reactant == 0 or n_product == 0:
                raise Exception(
                    f"{self.element_balance[element]} is not present on both "
                    "sides of chemical equation!"
                )

    def balance_equation(self, nth_decimal: int = ROUND_TO_NTH_DECIMAL) -> List[float]:
        """Determines coefficients for each molecule in balanced equation.

        Args:
            nth_decimal (int, optional): Round coefficients to nth decimal. Defaults to
                :param:`ROUND_TO_NTH_DECIMAL`.

        Returns:
            List[float]: Coefficients for each molecule in balanced chemical equation,
                rounded to ROUND_TO_NTH_DECIMAL.
        """
        all_coeff = np.array([balance for balance in self.element_balance.values()])
        n, _ = all_coeff.shape
        result = lsq_linear(
            all_coeff, np.zeros(n), bounds=(1, np.inf), tol=SOLUTION_TOLERANCE
        )
        if result.cost > SOLUTION_TOLERANCE:
            raise Exception(
                f"Could not find balanced equation. Coefficient matrix A was:"
                f"\n\n{all_coeff}\n\nOptimization result was:\n\n{result}\n"
            )
        x = result.x
        min_coeff = x.min()
        if min_coeff > 1:
            x *= 1 / min_coeff
        return x.round(nth_decimal).tolist()

    def _format_result(self, eq_side: List[str]) -> str:
        """Formats balanced coefficients for each molecule.

        Args:
            eq_side (List[str]): Molecules on given side of equation. Assumed that this
                method is called by :meth:`__init__` twice in reactant, product order,
                and that :attr:`self._eq_side_is_product` tracks which side is being
                processed.

        Returns:
            str: Formatted string containing molecules on given side of equation and
                their balanced coefficients.
        """
        coeff = self.balance
        if self._eq_side_is_product:
            coeff = coeff[len(self.molecules["reactants"]) :]  # noqa: E203
        self._eq_side_is_product = not self._eq_side_is_product
        combined = map(lambda coeff, molecule: f"{coeff} {molecule}", coeff, eq_side)
        full_str = " + ".join(combined)
        return full_str.replace("1.0 ", "")
