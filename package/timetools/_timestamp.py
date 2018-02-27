import datetime
import re
from pprint import pprint
from typing import Dict, Tuple, Union

# noinspection PyArgumentList
DateDictType = Dict[str, int]
DateTimeTuple = Tuple[int, int, int, int, int, int, int]
iso_date_pattern = """
	^
	(?P<iso>
		(?P<date>
			(?P<year>[\d]{4})
			[-]
			(?P<month>[\d]{1,2})
			[-]
			(?P<day>[\d]{1,2})
		)?
		[T\s]?
		(?P<time>
			(?P<hour>[\d]{0,2})
			[:]
			(?P<minute>[\d]{0,2})
			[:]
			(?P<second>[\d]{0,2})
		)?
	)
"""

regular_date_pattern = """"""

class Timestamp(datetime.datetime):
	timestamp_regex = r"""(?:(?P<year>[\d]{4})-(?P<month>[\d]{2})-(?P<day>[\d]{2}))?
						[\sA-Za-z]?
						(?:(?P<hour>[\d]+)[:](?P<minute>[\d]+)[:](?P<second>[\d]+))?"""
	timestamp_regex = re.compile(timestamp_regex, re.VERBOSE)

	verbal_regex = r"""(?P<first>[\dA-Za-z]+)[,\s]*(?P<second>[\dA-Za-z]+)[,\s]*(?P<year>[\d]+)"""
	verbal_regex = re.compile(verbal_regex, re.VERBOSE)

	def __new__(cls, *args, **kwargs):
		if len(args) == 1:
			result = cls._parseInput(args[0])
		elif len(args) == 3:
			result = {'year': args[0], 'month': args[1], 'day': args[2]}
			result.update(kwargs)
		elif len(args) != 0:
			result = args
		else:
			result = kwargs
		if isinstance(result, dict):
			# noinspection PyArgumentList
			return super().__new__(
				cls,
				result['year'], result['month'], result['day'],
				result.get('hour', 0), result.get('minute', 0), result.get('second', 0))
		else:
			# noinspection PyArgumentList
			return super().__new__(cls, *result)

	def __str__(self):
		string = self.toIso(True)
		return string

	def __repr__(self):
		string = "Timestamp('{}')".format(self.toiso())
		return string

	@staticmethod
	def _cleandict(item: Dict[Union[str,bytes], Union[int,str]]) -> Dict[str, int]:
		item = {k: (int(v) if v else 0) for k, v in item.items()}
		return item

	@classmethod
	def _parseExcel(cls, value: int) -> Dict[str, int]:
		value += datetime.date(year = 1899, month = 12, day = 30).toordinal()

		xldate, xltime = divmod(value, 1)
		date = datetime.date.fromordinal(int(xldate))
		# ------------------Convert Time------------------
		second = xltime * (3600 * 24)
		second = int(second)
		hour, second = divmod(second, 3600)
		minute, second = divmod(second, 60)

		result = {
			'year':   date.year,
			'month':  date.month,
			'day':    date.day,
			'hour':   hour,
			'minute': minute,
			'second': second
		}
		return result

	# Methods for converting generic datetime objects
	@classmethod
	def _parseGenericObject(cls, value):
		generic_date = cls._parseGenericDateObject(value)
		generic_time = cls._parseGenericTimeObject(value)
		if generic_date is None:
			message = "Invalid Date Object: {}".format(value)
			raise ValueError(message)
		generic_date.update(generic_time)
		return generic_date

	@classmethod
	def _parseGenericDateObject(cls, element):
		try:
			date_values = {
				'year':  element.year,
				'month': element.month,
				'day':   element.day
			}
		except AttributeError:
			date_values = None
		return date_values

	@classmethod
	def _parseGenericTimeObject(cls, element):
		try:
			time_values = {
				'hour':   element.hour,
				'minute': element.minute,
				'second': element.second
			}
		except AttributeError:
			time_values = dict()
		return time_values

	@classmethod
	def _parseInput(cls, value)->Dict[str,int]:
		if isinstance(value, str):
			result = cls._parseDateTimeString(value)
		elif isinstance(value, (tuple, list)):
			result = cls._parseTuple(value)
		elif isinstance(value, dict):
			result = cls._parseDict(value)
		else:
			result = cls._parseGenericObject(value)

		return result
	@classmethod
	def _parseDict(cls, value):
		return value
	@classmethod
	def _parseDateTimeString(cls, string: str) -> Dict[str, int]:
		""" parses a string formatted as a generic YY/MM/DD string. """
		if '-' in string or ':' in string:
			result = cls._parseTimestamp(string)
		elif ' ' in string:
			result = cls._parseVerbalDate(string)
		else:
			result = cls._parseNumericString(string)
		return result

	@classmethod
	def _parseNumericString(cls, string: str) -> Dict[str, int]:
		""" Parses a date formatted as YY[YY]MMDD. """
		extra, day = string[:-2], string[-2:]
		year, month = extra[:-2], extra[-2:]
		debug_info = {
			'string': string,
			'year':   year,
			'month':  month,
			'day':    day
		}
		pprint(debug_info)
		year = int(year)
		if year < 100:
			if year < 20:
				year += 2000
			else:
				year += 1900

		result = {
			'year':   int(year),
			'month':  int(month),
			'day':    int(day),
			'hour':   0,
			'minute': 0,
			'second': 0
		}
		return result

	@classmethod
	def _parseTimestamp(cls, string: str) -> Dict[str, int]:
		""" Parses a date and/or time formated as YYYY-MM-DDThh:mm:ss"""
		match = cls.timestamp_regex.search(string).groupdict()
		match = cls._cleandict(match)
		return match

	@classmethod
	def _parseTuple(cls, value: Tuple) -> Dict[str, int]:
		if len(value) == 3:
			keys = ('year', 'month', 'day')
		else:
			keys = ('year', 'month', 'day', 'hour', 'minute', 'second')
		datetime_dict = dict(zip(keys, value))
		return datetime_dict

	@classmethod
	def _parseVerbalDate(cls, value: str) -> Union[Dict[str, int],None]:
		# Parsed dates formatted verbally. Ex. 7 Oct 2015
		# print("Value: ", value)
		# print(cls.verbal_regex.search(value).groups())
		_short_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
		_long_months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
						'august', 'september', 'november', 'december']
		match = cls.verbal_regex.search(value)
		if not match:
			return None
		else:
			match = match.groups()
		_first, _second, _year = match
		if _first.isdigit():
			_day = _first
			_month = _second
		else:
			_day = _second
			_month = _first
		_month = _month.lower()

		if _month in _short_months:
			_months = _short_months
		else:
			_months = _long_months
		_month = _months.index(_month) + 1

		result = {
			'year':  int(_year),
			'month': int(_month),
			'day':   int(_day)
		}
		return result

	# Public access methods
	def getDate(self) -> Tuple[int, int, int]:
		return self.year, self.month, self.day

	def getTime(self) -> Tuple[int, int, int, int]:
		return self.hour, self.minute, self.second, self.microsecond

	def toiso(self, compact: bool = True) -> str:
		result = self.isoformat()
		if compact and not any(i != 0 for i in self.getTime()):
			result = result.split('T')[0]
		return result

	def toIso(self, compact: bool = True) -> str:
		# for compatability with the other methods names.
		return self.toiso(compact)

	def fromString(self, string):
		pass

	def fromObject(self, item):
		pass

	def toDict(self) -> Dict[str, int]:

		struct = self.timetuple()

		result = {
			# Regular
			'year':            struct.tm_year,
			'month':           struct.tm_mon,
			'day':             struct.tm_mday,
			'hour':            struct.tm_hour,
			'minute':          struct.tm_min,
			'second':          struct.tm_sec,
			'microsecond':     0,

			'daylightSavings': struct.tm_isdst,
			'ordinalDay':      struct.tm_yday,
			'weekDay':         struct.tm_wday,
			'timezone':        struct.tm_zone

		}
		return result

	def toTuple(self) -> DateTimeTuple:
		result = (
			self.year, self.month, self.day,
			self.hour, self.minute, self.second, self.microsecond
		)
		return result

	def toYear(self) -> float:
		""" Converts the timestamp to a float """

		data = self.toDict()

		year = data['year']

		ordinal_day = data['ordinalDay']
		if ordinal_day >= 364: ordinal_day = 364

		result = year + ((ordinal_day - 1) / 365)

		return result

	def toDatetime(self) -> datetime.datetime:
		return datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)


if __name__ == "__main__":
	stringa = "2018-11-13"
	stringb = "2018-02-24T19:49:24+00:00"
	stringc = None

	print(Timestamp(stringa))
	print(Timestamp(stringb))
	print(Timestamp(stringc))
	help(Timestamp.toiso)
