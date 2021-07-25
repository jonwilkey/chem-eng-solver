import re
from typing import Dict, List

import numpy as np

REGEX = {
    "molecules": re.compile("([A-Za-z0-9]+)"),
    "elements": re.compile("([A-Z][a-z]?)([0-9]*)"),
}


class Stoichiometry:
    """
    Provides methods for balances chemical equations
    """

    def __init__(self, input_eq: str) -> None:
        """
        Initialize class and parse input equation to find stoichiometrically
        balanced version on input equation.

        Args:
            input_eq (str): Input equation, e.g. "CH4 + O2 --> CO2 + H2O". Input
                does not need to be balanced (in fact input coefficients are
                ignored). Must contain a ">" character, which is used to
                identify reactants vs. products.

        Raises:
            Exception: if input_str does not contain a ">" character
        """
        if ">" not in input_eq:
            raise Exception(
                f"The input:\n\n{input_eq}\n\ndoes not contain a '>' character"
            )
        self.input_eq = input_eq
        self.element_balance: Dict[str, List[float]] = {
            element: [] for element, _ in REGEX["elements"].findall(input_eq)
        }
        reactants, products = input_eq.split(">")
        self._parse_eq(reactants)
        self._parse_eq(products, is_product=True)
        self.balance = np.array(
            [balance for balance in self.element_balance.values()]
        )

    def _parse_eq(self, eq: str, is_product: bool = False) -> None:
        """
        Method for parsing components of the input chemical equation to find how
        many of each unique element type are present in each reactant/product
        molecule, updating `self.element_balance` accordingly.

        Args:
            eq (str): Component of input equation (either reactant or product)
            is_product (bool, optional): Whether or not :param:`eq` is from the
                product side of the chemical equation. Defaults to False. If it
                is the product, then all coefficients in the elemental balance
                for parsed molecules on the reactant set will be given a
                negative value.
        """
        for molecule in REGEX["molecules"].findall(eq):
            composition = {k: v for k, v in REGEX["elements"].findall(molecule)}
            for element in self.element_balance.keys():
                count = composition.get(element)
                if count is None:
                    count = 0.0
                else:
                    count = 1.0 if count == "" else float(count)
                    if is_product:
                        count *= -1.0
                self.element_balance[element].append(count)
