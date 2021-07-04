import re
from typing import Tuple, Union

import unyt as u


class Patterns:
    """
    Define regular expressions used for parsing input_strings here
    """
    initial = re.compile(r"^([-0-9\.]+)\s+([a-zA-Z)^/*0-9\s-]+)")
    base_units = re.compile(r"([a-zA-Z]+)")
    operators = r"(^[\*/]?{unit}\^?(-?\d+)?)"


def _initial_parser(input_str: str) -> Tuple[float, str]:
    """
    Parses input into numeric value string and units string.

    Args:
        input_str (str): Input string

    Raises:
        Exception: If input string doesn't match expected pattern

    Returns:
        Tuple[float, str]: Value and units of parsed input string
    """
    found = Patterns.initial.findall(input_str)
    if not found:
        raise Exception(
            f"Input string '{input_str}' doesn't match expected parsing pattern"
            ". Please input value again using the pattern: '[-0-9\\.]+ [units]'"
            " where units are any set of character strings with '/' to indicate"
            " division and '**' or '^' are used to indicate exponentiation."
        )
    value, units = found[0]
    return float(value), units


def _units_parser(units: str) -> u.unyt_quantity:
    """
    Parses given units string, returning equivalent unyt_quantity object.

    Args:
        units (str): Units string, e.g. "kg/m/s**2"

    Raises:
        Exception: If unknown pattern is encountered that prevents function from
            building final_unit object (expects just multiplication, division,
            and exponentiation without paranthesis or brackets).

    Returns:
        u.unyt_quantity: unyt_quantity object equivalent to the input string.
    """
    units = units.replace(" ", "").replace("**", "^")
    final_units = 1.0
    for unit in Patterns.base_units.findall(units):
        base_unit = getattr(u, unit)
        parsed = re.findall(Patterns.operators.format(unit=unit), units)
        if not parsed:
            raise Exception(
                f"Cannot determine how to build '{unit}' into final_units from "
                f"first occurence in remaining unit string: {units}"
            )
        base_str, exponent = parsed[0]
        if base_str.startswith("/"):
            if exponent:
                final_units /= base_unit ** int(exponent)
            else:
                final_units /= base_unit
        else:
            if exponent:
                final_units *= base_unit ** int(exponent)
            else:
                final_units *= base_unit
        units = units.replace(base_str, "", 1)
    return final_units


def unit_converter(
    input_str: str, include_units: bool = False
) -> Union[float, u.unyt_quantity]:
    """
    Parses input value plus string and returns input converted into equivalent
    SI units. This function assumes that inputs match the following pattern:

    [0-9]+ [a-z]+([*/])?

    Args:
        input_str (str): Input value plus units, e.g. "212 degF"
        include_units (bool, optional): Whether or not to include units in the
            return object. Defaults to False.

    Returns:
        float: Value converted to SI units, e.g. "212 degF" --> 373.15 (the
            equivalent value in Kelvin)
    """
    value, units_str = _initial_parser(input_str)
    units = _units_parser(units_str)
    quantity = value * units
    quantity.convert_to_mks()
    return quantity if include_units else float(quantity.value)
