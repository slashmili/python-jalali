# -*- coding: utf-8 -*-
# jdatetime is (c) 2010-2011 Milad Rastian <eslashmili at gmail.com>.
# The jdatetime module was contributed to Python as of Python 2.7 and thus
# was licensed under the Python license. Same license applies to all files in
# the jdatetime package project.
from __future__ import unicode_literals
import datetime as py_datetime
import sys
from jdatetime.jalali import \
    GregorianToJalali, JalaliToGregorian, j_days_in_month
import re as _re
import locale as _locale
__VERSION__ = "1.7.1"
MINYEAR = 1
MAXYEAR = 9377

timedelta = py_datetime.timedelta
tzinfo = py_datetime.tzinfo

if sys.version_info[0] >= 3:  # py3
    _int_types = (int,)
else:
    _int_types = (int, long)


class time(py_datetime.time):

    def __repr__(self):
        return "jdatetime.time(%s, %s, %s)" % (self.hour,
                                               self.minute,
                                               self.second)


class date(object):
    """date(year, month, day) --> date object"""
    j_months_en = ['Farvardin',
                   'Ordibehesht',
                   'Khordad',
                   'Tir',
                   'Mordad',
                   'Shahrivar',
                   'Mehr',
                   'Aban',
                   'Azar',
                   'Dey',
                   'Bahman',
                   'Esfand']
    j_months_short_en = ['Far',
                         'Ord',
                         'Kho',
                         'Tir',
                         'Mor',
                         'Sha',
                         'Meh',
                         'Aba',
                         'Aza',
                         'Dey',
                         'Bah',
                         'Esf']

    j_weekdays_en = ['Shanbeh',
                     'Yekshanbeh',
                     'Doshanbeh',
                     'SehShanbeh',
                     'Chaharshanbeh',
                     'Panjshanbeh',
                     'Jomeh']
    j_weekdays_short_en = ['Sha',
                           'Yek',
                           'Dos',
                           'Seh',
                           'Cha',
                           'Pan',
                           'Jom']
    j_ampm_en = {'PM': 'PM', 'AM': 'AM'}

    j_months_fa = [u'فروردین',
                   u'اردیبهشت',
                   u'خرداد',
                   u'تیر',
                   u'مرداد',
                   u'شهریور',
                   u'مهر',
                   u'آبان',
                   u'آذر',
                   u'دی',
                   u'بهمن',
                   u'اسفند']
    j_months_short_fa = [u'فرو',
                         u'ارد',
                         u'خرد',
                         u'تیر',
                         u'مهر',
                         u'شهر',
                         u'مهر',
                         u'آبا',
                         u'آذر',
                         u'دی',
                         u'بهم',
                         u'اسف']

    j_weekdays_fa = [u'شنبه',
                     u'یکشنبه',
                     u'دوشنبه',
                     u'سه شنبه',
                     u'چهارشنبه',
                     u'پنجشنبه',
                     u'جمعه']
    j_weekdays_short_fa = [u'شنب',
                           u'یک',
                           u'دو',
                           u'سه',
                           u'چهار',
                           u'پنج',
                           u'جمع']
    j_ampm_fa = {'PM': u'بعد از ظهر', 'AM': u'قبل از ظهر'}

    if 'fa_IR' in _locale.getdefaultlocale():
        j_months = j_months_fa
        j_months_short = j_months_short_fa
        j_weekdays = j_weekdays_fa
        j_weekdays_short = j_weekdays_short_fa
        j_ampm = j_ampm_fa
    else:
        j_months = j_months_en
        j_months_short = j_months_short_en
        j_weekdays = j_weekdays_en
        j_weekdays_short = j_weekdays_short_en
        j_ampm = j_ampm_en

    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month

    @property
    def day(self):
        return self.__day

    __year = 0
    __month = 0
    __day = 0

    def _check_arg(self, value):
        if isinstance(value, _int_types):
            return True
        return False

    def __init__(self, year, month, day):
        """date(year, month, day) --> date object"""
        if not (self._check_arg(year) and
                self._check_arg(month) and
                self._check_arg(day)):
            raise TypeError("an integer is required" + repr(type(year)))
        if year < MINYEAR or year > MAXYEAR:
            raise ValueError("year is out of range")
        self.__year = year

        if month < 1 or month > 12:
            raise ValueError("month must be in 1..12")
        self.__month = month

        if day < 1:
            raise ValueError("day is out of range for month")
        if self.__month == 12 and day == 30 and self.isleap():
            # for leap years it's ok to have 30 days in Esfand
            pass
        elif self.__month == 12 and day == 30 and not self.isleap():
            raise ValueError("day is out of range for month")
        elif day > j_days_in_month[self.__month - 1]:
            raise ValueError("day is out of range for month")
        self.__day = day

    """The smallest possible difference between
    non-equal date objects, timedelta(days=1)."""
    resolution = timedelta(1)

    """The earliest representable date, date(MINYEAR, 1, 1)"""
    # min = date(MINYEAR, 1, 1)
    # TODO fixed errror:  name 'date' is not defined
    """The latest representable date, date(MAXYEAR, 12, 31)."""
    # max = date(MAXYEAR, 12,29)

    def isleap(self):
        """check if year is leap year
            algortim is based on http://en.wikipedia.org/wiki/Leap_year"""
        return self.year % 33 in (1, 5, 9, 13, 17, 22, 26, 30)

    def togregorian(self):
        """Convert current jalali date to gregorian and return datetime.date"""
        (y, m, d) = JalaliToGregorian(self.year,
                                      self.month,
                                      self.day).getGregorianList()
        return py_datetime.date(y, m, d)

    @staticmethod
    def fromgregorian(**kw):
        """Convert gregorian to jalali and return jdatetime.date
        jdatetime.date.fromgregorian(day=X,month=X,year=X)
        jdatetime.date.fromgregorian(date=datetime.date)
        """
        if 'date' in kw and isinstance(kw['date'], py_datetime.date):
            d = kw['date']
            (y, m, d) = GregorianToJalali(d.year,
                                          d.month,
                                          d.day).getJalaliList()
            return date(y, m, d)
        if 'day' in kw and 'month' in kw and 'year' in kw:
            (year, month, day) = (kw['year'], kw['month'], kw['day'])
            (y, m, d) = GregorianToJalali(year, month, day).getJalaliList()
            return date(y, m, d)

        error_msg = ["fromgregorian have to be be called"]
        error_msg += ["fromgregorian(day=X,month=X,year=X)"]
        error_msg += ["or"]
        error_msg += ["fromgregorian(date=datetime.date)"]
        raise ValueError(" ".join(error_msg))

    @staticmethod
    def today():
        """Current date or datetime:  same as self.__class__.fromtimestamp(time.time())."""
        to = py_datetime.date.today()
        (y, m, d) = GregorianToJalali(to.year,
                                      to.month,
                                      to.day).getJalaliList()
        return date(y, m, d)

    @staticmethod
    def fromtimestamp(timestamp):
        d = py_datetime.date.fromtimestamp(timestamp)
        (y, m, d) = GregorianToJalali(d.year, d.month, d.day).getJalaliList()
        return date(y, m, d)

    def toordinal(self):
        """Return proleptic jalali ordinal. Farvardin 1 of year 1 which is equal to 622-3-21 of Gregorian."""
        d = self.togregorian()
        return d.toordinal() - 226894

    @staticmethod
    def fromordinal(ordinal):
        """int -> date corresponding to a proleptic Jalali ordinal. it starts from Farvardin 1 of year 1, which is equal to 622-3-21 of Gregorian"""
        if ordinal < 1:
            raise ValueError("ordinal must be >= 1")
        d = py_datetime.date.fromordinal(226894 + ordinal)
        (y, m, d) = GregorianToJalali(d.year, d.month, d.day).getJalaliList()
        return date(y, m, d)

    def __repr__(self):
        return "jdatetime.date(%s, %s, %s)" % (self.year,
                                               self.month,
                                               self.day)

    def __str__(self):
        return self.strftime("%Y-%m-%d")

    def __add__(self, timedelta):
        """x.__add__(y) <==> x+y"""
        if not isinstance(timedelta, py_datetime.timedelta):
            raise TypeError(
                "unsupported operand type(s) for +: '%s' and '%s'" %
                (type(self), type(timedelta)))
        gd = self.togregorian() + timedelta
        return date.fromgregorian(date=gd)

    def __sub__(self, other):
        """x.__sub__(y) <==> x-y"""
        if isinstance(other, py_datetime.timedelta):
            gd = self.togregorian() - other
            return date.fromgregorian(date=gd)

        if isinstance(other, date):
            return self.togregorian() - other.togregorian()

        raise TypeError(
            "unsupported operand type(s) for -: '%s' and '%s'" %
            (type(self), type(timedelta)))

    def __radd__(self, timedelta):
        """x.__radd__(y) <==> y+x"""
        if not isinstance(timedelta, py_datetime.timedelta):
            raise TypeError(
                "unsupported operand type for +: '%s'" %
                (type(timedelta)))

        return self.__add__(timedelta)

    def __rsub__(self, other):
        """x.__rsub__(y) <==> y-x"""
        if isinstance(other, date):
            return self.__sub__(other)
        raise TypeError(
            "unsupported operand type for -: '%s'" %
            (type(other)))

    def __eq__(self, other_date):
        """x.__eq__(y) <==> x==y"""
        if other_date is None:
            return False
        if not isinstance(other_date, date):
            return False
        if self.year == other_date.year and \
           self.month == other_date.month and \
           self.day == other_date.day:
            return True
        return False

    def __ge__(self, other_date):
        """x.__ge__(y) <==> x>=y"""
        if not isinstance(other_date, date):
            raise TypeError(
                "unsupported operand type for >=: '%s'" %
                (type(other_date)))

        if self.year > other_date.year:
            return True
        elif self.year == other_date.year:
            if self.month > other_date.month:
                return True
            elif self.month == other_date.month and self.day >= other_date.day:
                return True
        return False

    def __gt__(self, other_date):
        """x.__gt__(y) <==> x>y"""
        if not isinstance(other_date, date):
            raise TypeError(
                "unsupported operand type for >: '%s'" %
                (type(other_date)))

        if self.year > other_date.year:
            return True
        elif self.year == other_date.year:
            if self.month > other_date.month:
                return True
            elif self.month >= other_date.month and self.day > other_date.day:
                return True
        return False

    def __le__(self, other_date):
        """x.__le__(y) <==> x<=y"""
        if not isinstance(other_date, date):
            raise TypeError(
                "unsupported operand type for <=: '%s'" %
                (type(other_date)))

        return not self.__ge__(other_date)

    def __lt__(self, other_date):
        """x.__lt__(y) <==> x<y"""
        if not isinstance(other_date, date):
            raise TypeError(
                "unsupported operand type for <: '%s'" %
                (type(other_date)))

        return not self.__gt__(other_date)

    def __ne__(self, other_date):
        """x.__ne__(y) <==> x!=y"""
        if other_date is None:
            return True
        if not isinstance(other_date, date):
            return True

        return not self.__eq__(other_date)

    def __hash__(self):
        """x.__hash__() <==> hash(x)"""
        gd = self.togregorian()
        return gd.__hash__()

    def ctime(self):
        """Return ctime() style string."""
        return self.strftime("%c")

    def replace(self, year=0, month=0, day=0):
        """Return date with new specified fields."""
        new_year = self.year
        new_month = self.month
        new_day = self.day

        if year != 0:
            new_year = year
        if month != 0:
            new_month = month
        if day != 0:
            new_day = day

        return date(new_year, new_month, new_day)

    def yday(self):
        """return day of year"""
        day = 0
        for i in range(0, self.month - 1):
            day = day + j_days_in_month[i]
        day = day + self.day
        return day

    def weekday(self):
        """Return the day of the week represented by the date.
        Shanbeh == 0 ... Jomeh == 6"""
        gd = self.togregorian()
        if gd.weekday() == 5:
            return 0
        if gd.weekday() == 6:
            return 1
        if gd.weekday() == 0:
            return 2
        if gd.weekday() == 1:
            return 3
        if gd.weekday() == 2:
            return 4
        if gd.weekday() == 3:
            return 5
        if gd.weekday() == 4:
            return 6

    def isoweekday(self):
        """Return the day of the week as an integer, where Shanbeh is 1 and Jomeh is 7"""
        return self.weekday() + 1

    def weeknumber(self):
        """Return week number """
        return self.yday() // 7

    def isocalendar(self):
        """Return a 3-tuple, (ISO year, ISO week number, ISO weekday)."""
        return (self.year, self.weeknumber(), self.isoweekday())

    def isoformat(self):
        """Return a string representing the date in ISO 8601 format, 'YYYY-MM-DD'"""
        return self.strftime("%Y-%m-%d")

    def __format__(self, format):
        """
        PEP-3101
        Make string formating work!
        """
        return self.strftime(format)

    # TODO: create jtime !
    # def timetuple(self):
    #    pass
    def strftime(self, format):
        """format -> strftime() style string."""
        # TODO: change stupid str.replace
        # formats = {
        #           '%a': lambda: self.j_weekdays_short[self.weekday()]
        # }
        # find all %[a-zA-Z] and call method if it in formats
        format = format.replace("%a", self.j_weekdays_short[self.weekday()])

        format = format.replace("%A", self.j_weekdays[self.weekday()])

        format = format.replace("%b", self.j_months_short[self.month - 1])

        format = format.replace("%B", self.j_months[self.month - 1])

        if '%c' in format:
            format = format.replace(
                "%c", self.strftime("%a %b %d %H:%M:%S %Y"))

        format = format.replace("%d", '%02.d' % (self.day))

        try:
            format = format.replace("%f", '%06.d' % (self.microsecond))
        except:
            format = format.replace("%f", "000000")

        try:
            format = format.replace("%H", '%02.d' % (self.hour))
        except:
            format = format.replace("%H", '00')

        try:
            if self.hour > 12:
                format = format.replace("%I", '%02.d' % (self.hour - 12))
            else:
                format = format.replace("%I", '%02.d' % (self.hour))
        except:
            format = format.replace("%I", '00')

        format = format.replace("%j", '%03.d' % (self.yday()))

        format = format.replace("%m", '%02.d' % (self.month))

        try:
            format = format.replace("%M", '%02.d' % (self.minute))
        except:
            format = format.replace("%M", '00')

        try:
            if self.hour > 12:
                format = format.replace("%p", self.j_ampm['PM'])
            else:
                format = format.replace("%p", self.j_ampm['AM'])
        except:
            format = format.replace("%p", self.j_ampm['AM'])

        try:
            format = format.replace("%S", '%02.d' % (self.second))
        except:
            format = format.replace("%S", '00')

        format = format.replace("%w", str(self.weekday()))

        format = format.replace("%W", str(self.weeknumber()))

        if '%x' in format:
            format = format.replace("%x", self.strftime("%m/%d/%y"))

        if '%X' in format:
            format = format.replace("%X", self.strftime('%H:%I:%S'))

        format = format.replace("%Y", str(self.year))

        format = format.replace("%y", str(self.year)[2:])

        format = format.replace("%Y", str(self.year))

        try:
            sign = "+"
            diff = self.tzinfo.utcoffset(self.tzinfo)
            diff_sec = diff.seconds
            if diff.days > 0 or diff.days < -1:
                raise ValueError(
                    "tzinfo.utcoffset() returned big time delta! ; must be in -1439 .. 1439")
            if diff.days != 0:
                sign = "-"
                diff_sec = (1 * 24 * 60 * 60) - diff_sec
            tmp_min = diff_sec / 60
            diff_hour = tmp_min / 60
            diff_min = tmp_min % 60
            format = format.replace(
                "%z", '%s%02.d%02.d' %
                (sign, diff_hour, diff_min))
        except AttributeError:
            format = format.replace("%z", '')

        try:
            format = format.replace("%Z", self.tzinfo.tzname(self.tzinfo))
        except AttributeError:
            format = format.replace("%Z", '')

        return format


class datetime(date):
    """datetime(year, month, day, [hour, [minute, [seconds, [microsecond, [tzinfo]]]]]) --> datetime objects"""
    __time = None

    def time(self):
        """Return time object with same time but with tzinfo=None."""
        return time(self.hour, self.minute, self.second, self.microsecond)

    def date(self):
        """Return date object with same year, month and day."""
        return date(self.year, self.month, self.day)

    def __init__(
            self,
            year,
            month,
            day,
            hour=None,
            minute=None,
            second=None,
            microsecond=None,
            tzinfo=None):
        date.__init__(self, year, month, day)
        tmp_hour = 0
        tmp_min = 0
        tmp_sec = 0
        tmp_micr = 0
        if hour is not None:
            tmp_hour = hour
        if minute is not None:
            tmp_min = minute
        if second is not None:
            tmp_sec = second
        if microsecond is not None:
            tmp_micr = microsecond

        if not (self._check_arg(tmp_hour) and self._check_arg(tmp_min) and
                self._check_arg(tmp_sec) and self._check_arg(tmp_micr)):
            raise TypeError("an integer is required")

        self.__time = time(tmp_hour, tmp_min, tmp_sec, tmp_micr, tzinfo)

    def __repr__(self):
        if self.__time.tzinfo is not None:
            return "jdatetime.datetime(%s, %s, %s, %s, %s, %s, %s, tzinfo=%s)" % (
                self.year,
                self.month,
                self.day, self.hour,
                self.minute,
                self.second,
                self.microsecond,
                self.tzinfo)

        if self.__time.microsecond != 0:
            return "jdatetime.datetime(%s, %s, %s, %s, %s, %s, %s)" % (
                self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                self.second,
                self.microsecond)

        if self.__time.second != 0:
            return "jdatetime.datetime(%s, %s, %s, %s, %s, %s)" % (
                self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                self.second)

        return "jdatetime.datetime(%s, %s, %s, %s, %s)" % (
            self.year, self.month, self.day, self.hour, self.minute)

    @staticmethod
    def today():
        """Current date or datetime"""
        return datetime.now()

    @staticmethod
    def now(tz=None):
        """[tz] -> new datetime with tz's local day and time."""
        now_datetime = py_datetime.datetime.now(tz)
        now = date.fromgregorian(date=now_datetime.date())
        return datetime(
            now.year,
            now.month,
            now.day,
            now_datetime.hour,
            now_datetime.minute,
            now_datetime.second,
            now_datetime.microsecond,
            tz)

    @staticmethod
    def utcnow():
        """Return a new datetime representing UTC day and time."""
        now_datetime = py_datetime.datetime.utcnow()
        now = date.fromgregorian(date=now_datetime.date())
        return datetime(
            now.year,
            now.month,
            now.day,
            now_datetime.hour,
            now_datetime.minute,
            now_datetime.second,
            now_datetime.microsecond)

    @staticmethod
    def fromtimestamp(timestamp, tz=None):
        """timestamp[, tz] -> tz's local time from POSIX timestamp."""
        now_datetime = py_datetime.datetime.fromtimestamp(timestamp, tz)
        now = date.fromgregorian(date=now_datetime.date())
        return datetime(
            now.year,
            now.month,
            now.day,
            now_datetime.hour,
            now_datetime.minute,
            now_datetime.second,
            now_datetime.microsecond,
            tz)

    @staticmethod
    def utcfromtimestamp(timestamp):
        """timestamp -> UTC datetime from a POSIX timestamp (like time.time())."""
        now_datetime = py_datetime.datetime.fromtimestamp(timestamp)
        now = date.fromgregorian(date=now_datetime.date())
        return datetime(
            now.year,
            now.month,
            now.day,
            now_datetime.hour,
            now_datetime.minute,
            now_datetime.second,
            now_datetime.microsecond)

    @staticmethod
    def combine(d=None, t=None, **kw):
        """date, time -> datetime with same date and time fields"""

        c_date = None
        if d is not None:
            c_date = d
        elif 'date' in kw:
            c_date = kw['date']

        c_time = None
        if t is not None:
            c_time = t
        elif 'time' in kw:
            c_time = kw['time']

        if c_date is None:
            raise TypeError("Required argument 'date' (pos 1) not found")
        if c_time is None:
            raise TypeError("Required argument 'date' (pos 2) not found")

        if not isinstance(c_date, date):
            raise TypeError(
                "combine() argument 1 must be jdatetime.date, not %s" %
                (type(c_date)))
        if not isinstance(c_time, time):
            raise TypeError(
                "combine() argument 2 must be jdatetime.time, not %s" %
                (type(c_time)))

        return datetime(
            c_date.year,
            c_date.month,
            c_date.day,
            c_time.hour,
            c_time.minute,
            c_time.second,
            c_time.microsecond,
            c_time.tzinfo)

    @staticmethod
    def fromordinal(ordinal):
        """int -> date corresponding to a proleptic Jalali ordinal. it starts from Farvardin 1 of year 1, which is equal to 622-3-21 of Gregorian"""
        if ordinal < 1:
            raise ValueError("ordinal must be >= 1")
        d = py_datetime.date.fromordinal(226894 + ordinal)
        j_date = date.fromgregorian(date=d)
        return datetime(j_date.year, j_date.month, j_date.day, 0, 0)

    @property
    def hour(self):
        return self.__time.hour

    @property
    def minute(self):
        return self.__time.minute

    @property
    def second(self):
        return self.__time.second

    @property
    def microsecond(self):
        return self.__time.microsecond

    @property
    def tzinfo(self):
        return self.__time.tzinfo

    @staticmethod
    def strptime(date_string, format):
        """string, format -> new datetime parsed from a string (like time.strptime())"""
        if '*' in format:
            format = format.replace("*", "\*")
        if '+' in format:
            format = format.replace("+", "\+")
        if '(' in format or ')' in format:
            format = format.replace("(", "\(")
            format = format.replace(")", "\)")
        if '[' in format or ']' in format:
            format = format.replace("[", "\[")
            format = format.replace("]", "\]")
        result_date = {
            'day': 1,
            'month': 1,
            'year': 1279,
            'microsecond': 0,
            'second': 0,
            'minute': 0,
            'hour': 0}
        apply_order = []
        format_map = {
            '%d': ['[0-9]{1,2}', 'day'],
            '%f': ['[0-9]{1,6}', 'microsecond'],
            '%H': ['[0-9]{1,2}', 'hour'],
            '%m': ['[0-9]{1,2}', 'month'],
            '%M': ['[0-9]{1,2}', 'minute'],
            '%S': ['[0-9]{1,2}', 'second'],
            '%Y': ['[0-9]{4,5}', 'year'],
        }
        regex = format
        find = _re.compile("([%a-zA-Z]{2})")

        for form in find.findall(format):
            if form in format_map:
                regex = regex.replace(form, "(" + format_map[form][0] + ")")
                apply_order.append(format_map[form][1])
        try:
            p = _re.compile(regex)
            if not p.match(date_string):
                raise ValueError()
            for i, el in enumerate(p.match(date_string).groups()):
                result_date[apply_order[i]] = int(el)
            return datetime(
                result_date['year'],
                result_date['month'],
                result_date['day'],
                result_date['hour'],
                result_date['minute'],
                result_date['second'])
        except:
            raise ValueError(
                "time data '%s' does not match format '%s'" %
                (date_string, format))

    def replace(
            self,
            year=None,
            month=None,
            day=None,
            hour=None,
            minute=None,
            second=None,
            microsecond=None,
            tzinfo=None):
        """Return datetime with new specified fields."""
        t_year = self.year
        if year is not None:
            t_year = year

        t_month = self.month
        if month is not None:
            t_month = month

        t_day = self.day
        if day is not None:
            t_day = day

        t_hour = self.hour
        if hour is not None:
            t_hour = hour

        t_min = self.minute
        if minute is not None:
            t_min = minute

        t_sec = self.second
        if second is not None:
            t_sec = second

        t_mic = self.microsecond
        if microsecond is not None:
            t_mic = microsecond

        t_tz = self.tzinfo
        if tzinfo is not None:
            t_tz = t_tz
        return datetime(
            t_year,
            t_month,
            t_day,
            t_hour,
            t_min,
            t_sec,
            t_mic,
            t_tz)

    def __add__(self, timedelta):
        """x.__add__(y) <==> x+y"""
        if isinstance(timedelta, py_datetime.timedelta):
            return self.__calculation_on_timedelta('__add__', timedelta)
        raise TypeError(
            "unsupported operand type(s) for +: '%s' and '%s'" %
            (type(self), type(timedelta)))

    def __sub__(self, other):
        """x.__sub__(y) <==> x-y"""
        if isinstance(other, py_datetime.timedelta):
            return self.__calculation_on_timedelta('__sub__', other)
        if isinstance(other, datetime):
            return self.__calculation_on_datetime('__sub__', other)
        raise TypeError(
            "unsupported operand type(s) for -: '%s' and '%s'" %
            (type(self), type(other)))

    def __radd__(self, timedelta):
        """x.__radd__(y) <==> y+x"""
        if isinstance(timedelta, py_datetime.timedelta):
            return self.__add__(timedelta)
        raise TypeError(
            "unsupported operand type for +: '%s' and '%s'" %
            (type(py_datetime.timedelta), type(self)))

    def __rsub__(self, other):
        """x.__rsub__(y) <==> y-x"""
        if isinstance(other, datetime):
            return self.__calculation_on_datetime('__rsub__', other)

        raise TypeError(
            "unsupported operand type for -: '%s' and '%s'" %
            (type(other), type(self)))

    def __calculation_on_timedelta(self, action, timedelta):
        gdatetime = self.togregorian()
        new_gdatetime = getattr(gdatetime, action)(timedelta)

        return datetime.fromgregorian(datetime=new_gdatetime)

    def __calculation_on_datetime(self, action, another_datetime):
        self_gdatetime = self.togregorian()
        another_gdatetime = another_datetime.togregorian()

        return getattr(self_gdatetime, action)(another_gdatetime)

    def __eq__(self, other_datetime):
        """x.__eq__(y) <==> x==y"""
        if other_datetime is None:
            return False
        if not isinstance(other_datetime, datetime):
            return False
        if self.year == other_datetime.year and \
           self.month == other_datetime.month and \
           self.day == other_datetime.day:
            return self.timetz() == other_datetime.timetz(
            ) and self.microsecond == other_datetime.microsecond
        return False

    def __ge__(self, other_datetime):
        """x.__ge__(y) <==> x>=y"""
        if not isinstance(other_datetime, datetime):
            raise TypeError(
                "unsupported operand type for >=: '%s'" %
                (type(other_datetime)))

        return (self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                self.second,
                self.microsecond) >= \
            (other_datetime.year,
             other_datetime.month,
             other_datetime.day,
             other_datetime.hour,
             other_datetime.minute,
             other_datetime.second,
             other_datetime.microsecond)

    def __gt__(self, other_datetime):
        """x.__gt__(y) <==> x>y"""
        if not isinstance(other_datetime, datetime):
            raise TypeError(
                "unsupported operand type for >: '%s'" %
                (type(other_datetime)))

        return (self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                self.second,
                self.microsecond) > \
            (other_datetime.year,
             other_datetime.month,
             other_datetime.day,
             other_datetime.hour,
             other_datetime.minute,
             other_datetime.second,
             other_datetime.microsecond)

    def __hash__(self):
        """x.__hash__() <==> hash(x)"""
        gdt = self.togregorian()
        return gdt.__hash__()

    def __le__(self, other_datetime):
        """x.__le__(y) <==> x<=y"""
        if not isinstance(other_datetime, datetime):
            raise TypeError(
                "unsupported operand type for <=: '%s'" %
                (type(other_datetime)))

        return not self.__gt__(other_datetime)

    def __lt__(self, other_datetime):
        """x.__lt__(y) <==> x<y"""
        if not isinstance(other_datetime, datetime):
            raise TypeError(
                "unsupported operand type for <: '%s'" %
                (type(other_datetime)))
        return not self.__ge__(other_datetime)

    def __ne__(self, other_datetime):
        """x.__ne__(y) <==> x!=y"""
        if other_datetime is None:
            return True
        if not isinstance(other_datetime, datetime):
            return True

        return not self.__eq__(other_datetime)

    @staticmethod
    def fromgregorian(**kw):
        """Convert gregorian to jalali and return jdatetime.datetime
        jdatetime.date.fromgregorian(day=X,month=X,year=X,[hour=X, [minute=X, [second=X, [tzinfo=X]]]])
        jdatetime.date.fromgregorian(date=datetime.date)
        jdatetime.date.fromgregorian(datetime=datetime.datetime)
        """
        if 'date' in kw and isinstance(kw['date'], py_datetime.date):
            d = kw['date']
            (y, m, d) = GregorianToJalali(d.year,
                                          d.month,
                                          d.day).getJalaliList()
            return datetime(y, m, d)
        if 'datetime' in kw and isinstance(
                kw['datetime'], py_datetime.datetime):
            dt = kw['datetime']
            (y, m, d) = GregorianToJalali(
                dt.year, dt.month, dt.day).getJalaliList()
            return datetime(
                y,
                m,
                d,
                dt.hour,
                dt.minute,
                dt.second,
                dt.microsecond,
                dt.tzinfo)
        if 'day' in kw and 'month' in kw and 'year' in kw:
            (year, month, day) = (kw['year'], kw['month'], kw['day'])
            (y, m, d) = GregorianToJalali(year, month, day).getJalaliList()
            hour = None
            minute = None
            second = None
            microsecond = None
            tzinfo = None
            if 'hour' in kw:
                hour = kw['hour']
                if 'minute' in kw:
                    minute = kw['minute']
                    if 'second' in kw:
                        second = kw['second']
                        if 'microsecond' in kw:
                            microsecond = kw['microsecond']
                            if 'tzinfo' in kw:
                                tzinfo = kw['tzinfo']
            return datetime(y, m, d, hour, minute, second, microsecond, tzinfo)

        raise ValueError(
            "fromgregorian have to called fromgregorian(day=X,month=X,year=X, [hour=X, [minute=X, [second=X, [tzinfo=X]]]]) or fromgregorian(date=datetime.date) or fromgregorian(datetime=datetime.datetime)")

    def togregorian(self):
        """Convert current jalali date to gregorian and return datetime.datetime"""
        gdate = date.togregorian(self)
        return py_datetime.datetime.combine(gdate, self.__time)

    def astimezone(self, tz):
        """tz -> convert to local time in new timezone tz"""
        gdt = self.togregorian()
        gdt = gdt.astimezone(tz)
        return datetime.fromgregorian(datetime=gdt)

    def ctime(self):
        """Return ctime() style string."""
        return self.strftime("%c")

    # TODO: check what this def does !
    def dst(self):
        """Return self.tzinfo.dst(self)"""
        if self.tzinfo:
            return self.tzinfo.dst(self)
        return None

    def isoformat(self):
        """[sep] -> string in ISO 8601 format, YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]."""
        mil = self.strftime("%f")
        if int(mil) == 0:
            mil = ""
        else:
            mil = "." + mil
        tz = self.strftime("%z")
        return self.strftime("%Y-%m-%dT%H:%M:%S") + "%s%s" % (mil, tz)

    def timetuple(self):
        """Return time tuple, compatible with time.localtime().
        It returns Gregorian object!
        """
        dt = self.togregorian()
        return dt.timetuple()

    def timetz(self):
        """Return time object with same time and tzinfo."""
        return self.__time

    def tzname(self):
        """Return self.tzinfo.tzname(self)"""
        if self.tzinfo:
            return self.tzinfo.tzname(self)
        return None

    def utcoffset(self):
        """Return self.tzinfo.utcoffset(self)."""
        if self.tzinfo:
            return self.tzinfo.utcoffset(self)

    def utctimetuple(self):
        """Return UTC time tuple, compatible with time.localtime().
        It returns Gregorian object !
        """
        dt = self.togregorian()
        return dt.utctimetuple()

    def __str__(self):
        mil = self.strftime("%f")
        if int(mil) == 0:
            mil = ""
        else:
            mil = "." + mil
        tz = self.strftime("%z")
        return self.strftime("%Y-%m-%d%H:%M:%S") + "%s%s" % (mil, tz)
