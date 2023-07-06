"""
	Convienient methods for converting between numbers and strings and number representations.
"""

import math
from numbers import Number
from typing import Any, Iterable, List, Union
import numpy

# from ._scale import scale
try:
	from . import _scale
except ImportError:
	import _scale
default_scale = _scale.DecimalScale()

NumberType = Union[int, float]


def _is_null(value) -> bool:
	if value is None or not isinstance(value, (int, float)):
		return True
	return False


def human_readable(value: NumberType, precision: int = 2) -> str:
	""" Converts a number into a more easily-read string.
		Ex. 101000 -> '101T' or (101, 'T')

		Parameters
		----------
		value: number, list<number>
			Any number or list of numbers. If a list is given, all numbers
			will be asigned the same suffix as the lowest number.
		precision: int; default 2
			The number of decimal places to show.

		Returns
		-------
		str, list<str>
			The reformatted number.
	"""
	template = '{0:.' + str(int(precision)) + 'f}{1}'
	magnitude = default_scale.get_magnitude_from_value(value)
	human_readable_number = value / magnitude.multiplier
	string = template.format(human_readable_number, magnitude.suffix)

	return string


def is_number(value: Union[Any, Iterable[Any]]) -> Union[bool, List[bool]]:
	"""Tests if the value is a number.

		Examples
		--------
		'abc'->False
		123.123 -> True
		'123.123' -> True

	"""
	if isinstance(value, (list, tuple)):
		return [is_number(i) for i in value]
	if isinstance(value, str):
		try:
			float(value)
			value_is_number = True
		except ValueError:
			value_is_number = False
	else:
		value_is_number = isinstance(value, Number)

	return value_is_number


def _convert_string_to_number(value: str, default = math.nan) -> float:
	if '/' in value:
		left, right = value.split('/')
		left = _convert_string_to_number(left)
		right = _convert_string_to_number(right)
		return left / right
	else:
		value = value.replace(',', '')  # Remove thousands separator.
		value = value.strip()
		try:
			value = float(value)
		except ValueError:
			value = default
		return value


def to_number(value: Union[Any, Iterable[Any]], default: Any = math.nan) -> Union[NumberType, List[NumberType]]:
	""" Attempts to convert the passed object to a number.
		Returns
		-------
			value: Scalar
				* list,tuple,set -> list of Number
				* int,float -> int, float
				* str -> int, float
				* generic -> float if float() works, else math.nan
	"""
	if isinstance(value, str):
		return _convert_string_to_number(value, default)

	if isinstance(value, (list, tuple, set)):
		return [to_number(i, default) for i in value]

	try:
		converted_number = float(value)
	except (ValueError, TypeError):
		converted_number = default

	if not _is_null(converted_number) and math.floor(converted_number) == converted_number:
		converted_number = int(converted_number)

	return converted_number


def convert_base(value: Union[int, str], before: int = 10, after: int = 10) -> Union[int, str]:
	intermediate = int(value, before)
	result = int(intermediate, after)
	return result


def to_decimal(value, base, lower = False, readable = False):
	""" Converts any number to base 10
		Parameters
		----------
			value: string
				The number to convert
			base: int
				The current base of the number
			readable: bool; default False
				Whether to omit similar symbols. Currently defunct
		Returns
		----------
			number: int
	"""
	Z = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	if lower:
		Z = Z.lower()
	if base < 37:
		return int(value, base)
	else:
		Z = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	digits = value[::-1]
	number = sum(Z.find(digit) * (base ** index) for index, digit in enumerate(digits))

	return number


def from_decimal(value, base, readable = False):
	""" Converts a number in Base 10 to another Base
		Parameters
		----------
			value: int
				The number (in base 10) to convert
			base: int
				The base to convert the number to
			readable: bool, default False
				Omits similar symbols. Currently non-working
		Returns
		----------
			number : string
	"""
	if base < 37:
		Z = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	else:
		Z = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	if base > len(Z):
		print("to_base({0}, {1})".format(value, base))
		raise ValueError("base must be >= 2 and <= {0}".format(len(Z)))
	_pythonic_bases = {2, 8, 16}
	if base in _pythonic_bases:
		if base == 2:
			number = '{0:b}'.format(value)
		elif base == 8:
			number = '{0:o}'.format(value)
		elif base == 16:
			number = '{0:X}'.format(value)
		return number

	bases = list()
	index = 0
	maximum = 1
	while maximum <= value:
		index += 1
		bases.append(maximum)
		maximum = pow(base, index)
	bases = bases[::-1]

	number = str()
	for ibase in bases:
		mod, value = divmod(value, ibase)
		number += Z[mod]
	return number


def convert_base(value, from_base, to_base):
	return from_decimal(to_decimal(value, from_base), to_base)


def normalize_values(values: numpy.ndarray) -> numpy.ndarray:
	"""
		Maps the values form the input into the domain [0,1]
	"""
	return (values - numpy.min(values)) / (numpy.max(values) - numpy.min(values))


def main():
	for i in range(100):
		result = from_decimal(i, 2)
		print(f"{i} - {result:>04}")
		if len(result) > 4:
			break


if __name__ == "__main__":
	main()
