from pytools.timetools._timestamp import Timestamp
from unittest import TestCase, main
import datetime


class TimestampTestSetup(TestCase):
	def setUp(self):
		self.key = datetime.datetime.now()
		# Key without microseconds
		self.mkey = datetime.datetime(self.key.year, self.key.month, self.key.day, self.key.hour, self.key.minute,
			self.key.second)
		self.datekey = datetime.datetime(self.key.year, self.key.month, self.key.day)

		self.year = self.key.year
		self.month = self.key.month
		self.day = self.key.day

		self.hour = self.key.hour
		self.minute = self.key.minute
		self.second = self.key.second
		self.microsecond = self.key.microsecond

		self.rtuple = (self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond)

		try:
			self.timestamp = Timestamp(self.key)
		except:
			self.timestamp = None


class TimestampParsingTest(TimestampTestSetup):
	def test_from_american_date(self):
		string = f"{self.month}/{self.day}/{self.year}"

		from_method = Timestamp.from_american_date(string)
		from_init = Timestamp(string)

		self.assertEqual(self.datekey, from_method)
		self.assertEqual(self.datekey, from_init)

	def test_from_verbal_date(self):
		pass

	def test_from_short_dict(self):
		sd = {
			'year':  self.year,
			'month': self.month,
			'day':   self.day
		}

		from_method1 = Timestamp.from_dict(**sd)
		from_method2 = Timestamp.from_keys(sd)
		from_init1 = Timestamp(**sd)
		from_init2 = Timestamp(sd)

		self.assertEqual(self.datekey, from_method1)
		self.assertEqual(self.datekey, from_method2)
		self.assertEqual(self.datekey, from_init1)
		self.assertEqual(self.datekey, from_init2)

	def test_from_long_dict(self):
		ld = {
			'year':        self.year,
			'month':       self.month,
			'day':         self.day,
			'hour':        self.hour,
			'minute':      self.minute,
			'second':      self.second,
			'microsecond': self.microsecond
		}

		from_method1 = Timestamp.from_dict(**ld)
		from_method2 = Timestamp.from_keys(ld)
		from_init1 = Timestamp(**ld)
		from_init2 = Timestamp(ld)

		self.assertEqual(self.key, from_method1)
		self.assertEqual(self.key, from_method2)
		self.assertEqual(self.key, from_init1)
		self.assertEqual(self.key, from_init2)

	def test_from_short_tuple(self):
		st = (self.year, self.month, self.day)
		from_method = Timestamp.from_tuple(st)
		from_init = Timestamp(st)
		self.assertEqual(self.datekey, from_method)
		self.assertEqual(self.datekey, from_init)

	def test_from_long_tuple(self):
		lt = (self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond)

		from_method = Timestamp.from_tuple(lt)
		from_init = Timestamp(lt)
		self.assertEqual(self.key, from_method)
		self.assertEqual(self.key, from_init)

	def test_from_values(self):
		args = (self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond)

		from_method = Timestamp.from_values(*args)
		from_init = Timestamp(*args)

		self.assertEqual(self.key, from_method)
		self.assertEqual(self.key, from_init)


class TimestampTypingTest(TimestampTestSetup):
	def test_from_obj_type(self):
		result = Timestamp.from_object(self.key)

		self.assertIsInstance(result, Timestamp)

	def test_from_dict(self):
		data = {
			'year':  self.year,
			'month': self.month,
			'day':   self.day
		}
		result = Timestamp.from_dict(**data)
		self.assertIsInstance(result, Timestamp)

	def test_from_values(self):
		result = Timestamp(*self.rtuple)


class TimestampRepresentTest(TimestampTestSetup):
	def test_to_iso(self):
		ts = Timestamp.from_object(self.mkey)

		self.assertEqual(ts, Timestamp(ts.to_iso()))


if __name__ == "__main__":
	main()