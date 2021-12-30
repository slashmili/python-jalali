# -*- coding: utf-8 -*-
import sys
import os
import time
import datetime
import platform
import threading
import locale
import unittest

try:
    import greenlet
    greenlet_installed = True
except ImportError:
    greenlet_installed = False

try:
    import zoneinfo
except ImportError:
    zoneinfo = None


BASEDIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
sys.path.insert(0, BASEDIR)
import jdatetime  # noqa


class GMTTime(jdatetime.tzinfo):
    def utcoffset(self, dt):
        return jdatetime.timedelta(hours=0)

    def tzname(self, dt):
        return "GMT"

    def dst(self, dt):
        return jdatetime.timedelta(0)


class TehranTime(jdatetime.tzinfo):
    def utcoffset(self, dt):
        return jdatetime.timedelta(hours=3, minutes=30)

    def tzname(self, dt):
        return "IRDT"

    def dst(self, dt):
        return jdatetime.timedelta(0)


class TestJDate(unittest.TestCase):
    def test_as_locale_returns_same_date_with_specified_locale(self):
        jdate_en = jdatetime.date(1397, 4, 23, locale='en_US')
        jdate_fa = jdate_en.aslocale('fa_IR')
        self.assertEqual(jdate_fa.year, 1397)
        self.assertEqual(jdate_fa.month, 4)
        self.assertEqual(jdate_fa.day, 23)
        self.assertEqual(jdate_fa.locale, 'fa_IR')

    def test_init_locale_is_effective_only_if_not_none(self):
        orig_locale = jdatetime.get_locale()
        jdatetime.set_locale('en_US')
        self.addCleanup(jdatetime.set_locale, orig_locale)
        date = jdatetime.date(1397, 4, 22, locale=None)
        self.assertEqual(date.locale, 'en_US')

    def test_init_locale_is_effective_only_if_not_empty(self):
        orig_locale = jdatetime.get_locale()
        jdatetime.set_locale('nl_NL')
        self.addCleanup(jdatetime.set_locale, orig_locale)
        date = jdatetime.date(1397, 4, 22, locale='')
        self.assertEqual(date.locale, 'nl_NL')

    def test_locale_property_is_read_only(self):
        date = jdatetime.date(1397, 4, 22)
        with self.assertRaises(AttributeError):
            date.locale = jdatetime.FA_LOCALE

    def test_locale_property_returns_locale(self):
        date = jdatetime.date(1397, 4, 22, locale='nl_NL')
        self.assertEqual(date.locale, 'nl_NL')

    def test_init_locale_is_named_argument_only(self):
        with self.assertRaises(TypeError):
            datetime.date(1397, 4, 22, 'nl_NL')

    def test_init_accepts_instance_locale(self):
        date = jdatetime.date(1397, 4, 23, locale=jdatetime.FA_LOCALE)
        self.assertEqual(date.strftime('%A'), u'شنبه')

    def test_dates_are_not_equal_if_locales_are_different(self):
        date_fa = jdatetime.date(1397, 4, 22, locale='fa_IR')
        date_nl = jdatetime.date(1397, 4, 22, locale='nl_NL')
        self.assertNotEqual(date_fa, date_nl)

    def test_fromgregorian_accepts_locale_keyword_arg_when_datetime_passed(self):
        today = datetime.datetime.today().date()
        j_today = jdatetime.date.fromgregorian(date=today, locale='nl_NL')
        self.assertEqual(j_today.locale, 'nl_NL')

    def test_fromgregorian_accepts_locale_keyword_arg_when_int_passed(self):
        j_today = jdatetime.date.fromgregorian(day=15, month=7, year=2018, locale='nl_NL')
        self.assertEqual(j_today.locale, 'nl_NL')

    def test_replace_keeps_the_locale_of_source_date(self):
        date = jdatetime.date(1397, 4, 22, locale='nl_NL')
        other_date = date.replace(day=20)
        self.assertEqual(other_date.day, 20)
        self.assertEqual(other_date.locale, 'nl_NL')

    def test_add_time_delta(self):
        date = jdatetime.date(1397, 4, 22, locale='nl_NL')
        new_date = date + datetime.timedelta(days=1)
        self.assertEqual(new_date.year, 1397)
        self.assertEqual(new_date.month, 4)
        self.assertEqual(new_date.day, 23)
        self.assertEqual(new_date.locale, 'nl_NL')

    def test_reverse_add_time_delta(self):
        date = jdatetime.date(1397, 4, 22, locale='nl_NL')
        new_date = datetime.timedelta(days=2) + date
        self.assertEqual(new_date.year, 1397)
        self.assertEqual(new_date.month, 4)
        self.assertEqual(new_date.day, 24)
        self.assertEqual(new_date.locale, 'nl_NL')

    def test_subtract_time_delta(self):
        date = jdatetime.date(1397, 4, 22, locale='nl_NL')
        new_date = date - datetime.timedelta(days=1)
        self.assertEqual(new_date.year, 1397)
        self.assertEqual(new_date.month, 4)
        self.assertEqual(new_date.day, 21)
        self.assertEqual(new_date.locale, 'nl_NL')

    def test_subtract_datetime_date(self):
        date = jdatetime.date(1397, 4, 22, locale='nl_NL')
        delta = date - datetime.date(2018, 7, 12)
        self.assertEqual(delta.days, 1)

    def test_timetuple(self):
        date = jdatetime.date(1397, 4, 22,)
        self.assertEqual(
            date.timetuple(),
            time.struct_time((2018, 7, 13, 0, 0, 0, 4, 194, -1)),
        )

    def test_all_weekdays(self):
        date = jdatetime.date(1394, 1, 1)  # it is saturday
        for i in range(7):  # test th whole week
            self.assertEqual((date + datetime.timedelta(days=i)).weekday(), i)

    def test_max_year(self):
        dmax = jdatetime.date.max
        self.assertTrue(isinstance(dmax, jdatetime.date))
        self.assertEqual(dmax.year, jdatetime.MAXYEAR)
        self.assertRaises(ValueError, jdatetime.date, jdatetime.MAXYEAR + 1, 1, 1)
        with self.assertRaises(ValueError, msg="Should raise an exception when we go over date.max"):
            _ = dmax + jdatetime.date.resolution

    def test_min_year(self):
        dmin = jdatetime.date.min
        self.assertTrue(isinstance(dmin, jdatetime.date))
        self.assertEqual(dmin.year, jdatetime.MINYEAR)
        self.assertRaises(ValueError, jdatetime.date, jdatetime.MINYEAR - 1, 1, 1)
        with self.assertRaises(ValueError, msg="Should raise an exception when we ge below date.min"):
            _ = dmin - jdatetime.date.resolution


class TestJDateTime(unittest.TestCase):
    def test_datetime_date_method_keeps_datetime_locale_on_date_instance(self):
        datetime = jdatetime.datetime(1397, 4, 22, locale='nl_NL')
        date = datetime.date()
        self.assertEqual(date.locale, 'nl_NL')

    def test_init_locale_is_effective_only_if_not_none(self):
        orig_locale = jdatetime.get_locale()
        jdatetime.set_locale('en_US')
        self.addCleanup(jdatetime.set_locale, orig_locale)
        datetime = jdatetime.datetime(1397, 4, 22, locale=None)
        self.assertEqual(datetime.locale, 'en_US')

    def test_init_locale_is_effective_only_if_not_empty(self):
        orig_locale = jdatetime.get_locale()
        jdatetime.set_locale('nl_NL')
        self.addCleanup(jdatetime.set_locale, orig_locale)
        datetime = jdatetime.datetime(1397, 4, 22, locale='')
        self.assertEqual(datetime.locale, 'nl_NL')

    def test_locale_property_is_read_only(self):
        datetime = jdatetime.datetime(1397, 4, 22)
        with self.assertRaises(AttributeError):
            datetime.locale = jdatetime.FA_LOCALE

    def test_locale_property_returns_locale(self):
        datetime = jdatetime.datetime(1397, 4, 22, locale='nl_NL')
        self.assertEqual(datetime.locale, 'nl_NL')

    def test_init_locale_is_named_argument_only(self):
        with self.assertRaises(TypeError):
            datetime.datetime(1397, 4, 22, 'nl_NL')

    def test_init_accepts_instance_locale(self):
        datetime = jdatetime.datetime(1397, 4, 23, locale=jdatetime.FA_LOCALE)
        self.assertEqual(datetime.strftime('%A'), u'شنبه')

    def test_today(self):
        today = datetime.date.today()
        converted_today = jdatetime.date.today().togregorian()
        self.assertEqual(today.year, converted_today.year)

    def test_fromtimestamp(self):
        d = jdatetime.date.fromtimestamp(1783232224)
        self.assertEqual(1405, d.year)
        self.assertEqual(4, d.month)
        self.assertEqual(14, d.day)

    def test_fromordinal(self):
        d = jdatetime.date.fromordinal(1)
        self.assertEqual(1, d.year)

    def test_comparison(self):
        today = jdatetime.date.today()
        self.assertEqual(False, today < today - jdatetime.timedelta(days=76))
        self.assertEqual(False, today <= today - jdatetime.timedelta(days=1))
        self.assertEqual(True, today + jdatetime.timedelta(days=1) > today)
        self.assertEqual(True, today + jdatetime.timedelta(days=30) >= today)
        self.assertEqual(True, today == today)
        self.assertEqual(False, today > today)
        self.assertEqual(False, today < today)
        self.assertEqual(True, today >= today)
        self.assertEqual(True, today <= today)
        not_today = jdatetime.date(today.year, today.month, today.day) + jdatetime.timedelta(days=1)
        self.assertEqual(True, today != not_today)

        dtg = jdatetime.datetime(1380, 12, 1, 1, 2, 4)
        self.assertEqual(True, dtg < dtg + jdatetime.timedelta(seconds=1))
        self.assertEqual(True, dtg - jdatetime.timedelta(seconds=1) < dtg)
        self.assertEqual(False, dtg is None)

    def test_date_conversion_date_input(self):
        # todo: add some corner cases
        d1 = datetime.date(2010, 11, 23)
        jd1 = jdatetime.date(1389, 9, 2)
        d2 = datetime.date(2011, 5, 13)
        jd2 = jdatetime.date(1390, 2, 23)

        self.assertEqual(d1, jd1.togregorian())
        self.assertEqual(d2, jd2.togregorian())
        self.assertEqual(jd1, jdatetime.date.fromgregorian(date=d1))
        self.assertEqual(jd2, jdatetime.date.fromgregorian(date=d2))

    def test_date_conversion_integer_input(self):
        d_check_with = jdatetime.date(1390, 2, 23)
        jd_datetime = jdatetime.datetime.fromgregorian(
            year=2011,
            month=5,
            day=13,
            hour=14,
            minute=15,
            second=16,
        )
        self.assertEqual(
            True,
            jd_datetime == jdatetime.datetime.combine(d_check_with, jdatetime.time(14, 15, 16))
        )

        gdatetime = datetime.datetime(2011, 5, 13, 14, 15, 16)
        self.assertEqual(True, jd_datetime.togregorian() == gdatetime)

    def test_strftime(self):
        s = jdatetime.date(1390, 2, 23)
        string_format = "%a %A %b %B %c %d %H %I %j %m %M %p %S %w %W %x %X %y %Y %f %z %Z"
        output = (
            'Fri Friday Ord Ordibehesht Fri Ord 23 00:00:00 '
            '1390 23 00 12 054 02 00 AM 00 6 8 02/23/90 00:00:00 90 1390 000000  '
        )
        self.assertEqual(s.strftime(string_format), output)

        dt = jdatetime.datetime(1390, 2, 23, 12, 13, 14, 1)
        unicode_format = "%a %A %b %B %c %d %H %I %j %m %M %p %S %w %W %x %X %y %Y %f"
        output = (
            'Fri Friday Ord Ordibehesht Fri Ord 23 12:13:14 '
            '1390 23 12 12 054 02 13 PM 14 6 8 02/23/90 12:13:14 90 1390 000001'
        )
        self.assertEqual(dt.strftime(unicode_format), output)

        dt = jdatetime.datetime(1390, 2, 23, 12, 13, 14, 1)
        string_format = u"ﺱﺎﻟ = %y، ﻡﺎﻫ = %m، ﺭﻭﺯ = %d"
        output = u"ﺱﺎﻟ = 90، ﻡﺎﻫ = 02، ﺭﻭﺯ = 23"
        self.assertEqual(dt.strftime(string_format), output)

        class NYCTime(jdatetime.tzinfo):
            def utcoffset(self, dt):
                return jdatetime.timedelta(hours=-4)

            def tzname(self, dt):
                return "EDT"

            def dst(self, dt):
                return jdatetime.timedelta(0)

        nyc = NYCTime()
        dt = jdatetime.datetime(1389, 2, 17, 19, 10, 2, tzinfo=nyc)
        self.assertEqual(True, dt.strftime("%Z %z") == "EDT -0400")

        teh = TehranTime()
        dt = jdatetime.datetime(1389, 2, 17, 19, 10, 2, tzinfo=teh)
        self.assertEqual(True, dt.strftime("%Z %z") == "IRDT +0330")

    def test_strftime_unicode(self):
        s = jdatetime.date(1390, 2, 23)
        self.assertEqual(s.strftime("%a %A".encode("utf-8")), "Fri Friday")

    def test_kabiseh(self):
        kabiseh_year = jdatetime.date.fromgregorian(date=datetime.date(2013, 3, 20))
        self.assertEqual(True, kabiseh_year.isleap() is True)

        normal_year = jdatetime.date.fromgregorian(date=datetime.date(2014, 3, 20))
        self.assertEqual(True, normal_year.isleap() is False)

        kabiseh_year = jdatetime.date(1391, 12, 30)
        self.assertEqual(True, kabiseh_year.isleap() is True)

        with self.assertRaises(ValueError):
            jdatetime.date(1392, 12, 30)

    def test_datetime(self):
        d = jdatetime.datetime(1390, 1, 2, 12, 13, 14)

        self.assertEqual(True, d.time() == jdatetime.time(12, 13, 14))
        self.assertEqual(True, d.date() == jdatetime.date(1390, 1, 2))

    def test_datetimetoday(self):
        jnow = jdatetime.datetime.today()
        today = datetime.datetime.today().date()
        gnow = jdatetime.date.fromgregorian(date=today)

        self.assertEqual(True, jnow.date() == gnow)

    def test_datetimefromtimestamp(self):
        t = time.time()
        jnow = jdatetime.datetime.fromtimestamp(t).date()
        gnow = datetime.datetime.fromtimestamp(t).date()

        self.assertEqual(True, jdatetime.date.fromgregorian(date=gnow) == jnow)

    def test_combine(self):
        t = jdatetime.time(12, 13, 14)
        d = jdatetime.date(1390, 4, 5)
        dt = jdatetime.datetime(1390, 4, 5, 12, 13, 14)

        self.assertEqual(True, jdatetime.datetime.combine(d, t) == dt)

    def test_combine_keeps_date_locale(self):
        t = jdatetime.time(11, 20, 30)
        d = jdatetime.date(1397, 4, 24, locale='nl_NL')
        self.assertEqual(jdatetime.datetime.combine(d, t).locale, 'nl_NL')

    def test_replace(self):
        dt = jdatetime.datetime.today()
        args = {
            'year': 1390,
            'month': 12,
            'day': 1,
            'hour': 13,
            'minute': 14,
            'second': 15,
            'microsecond': 1233,
        }
        dtr = dt.replace(**args)
        dtn = jdatetime.datetime(1390, 12, 1, 13, 14, 15, 1233)

        self.assertEqual(True, dtr == dtn)

    def test_replace_keeps_date_locale(self):
        dt = jdatetime.datetime(1397, 4, 24, locale='nl_NL')
        args = {'year': 1390, 'month': 12, 'hour': 13}
        self.assertEqual(dt.replace(**args).locale, 'nl_NL')

    def test_replace_remove_tzinfo(self):
        teh = TehranTime()
        dt = jdatetime.datetime(1397, 8, 17, 7, 54, 28, tzinfo=teh)
        dt_naive = dt.replace(tzinfo=None)
        self.assertEqual(dt_naive.tzinfo, None)

    def test_strptime(self):
        date_string = "1363-6-6 12:13:14"
        date_format = "%Y-%m-%d %H:%M:%S"
        dt1 = jdatetime.datetime.strptime(date_string, date_format)
        dt2 = jdatetime.datetime(1363, 6, 6, 12, 13, 14)

        self.assertEqual(True, dt1 == dt2)

    def test_strptime_bare(self):
        date_string = "13630606121314"
        date_format = "%Y%m%d%H%M%S"
        dt1 = jdatetime.datetime.strptime(date_string, date_format)
        dt2 = jdatetime.datetime(1363, 6, 6, 12, 13, 14)

        self.assertTrue(dt1 == dt2)

    def test_strptime_handles_alphabets_in_format(self):
        date_string = "1363-6-6T12:13:14"
        date_format = "%Y-%m-%dT%H:%M:%S"
        dt1 = jdatetime.datetime.strptime(date_string, date_format)
        dt2 = jdatetime.datetime(1363, 6, 6, 12, 13, 14)

        self.assertEqual(dt1, dt2)

    def test_strptime_special_chars(self):
        date_string = "[1363*6*6] ? (12+13+14)"
        date_format = "[%Y*%m*%d] ? (%H+%M+%S)"
        dt1 = jdatetime.datetime.strptime(date_string, date_format)
        dt2 = jdatetime.datetime(1363, 6, 6, 12, 13, 14)

        self.assertEqual(dt1, dt2)

    def test_strptime_small_y(self):
        date_string = "01/1/1"
        date_format = "%y/%m/%d"
        dt1 = jdatetime.datetime.strptime(date_string, date_format)
        dt2 = jdatetime.datetime(1401, 1, 1)

        self.assertEqual(dt1, dt2)

    def test_strptime_do_match_excessive_characters(self):
        self.assertRaises(
            ValueError, jdatetime.datetime.strptime, '21 ', '%y')

    def test_datetime_eq(self):
        date_string = "1363-6-6 12:13:14"
        date_format = "%Y-%m-%d %H:%M:%S"

        dt1 = jdatetime.datetime.strptime(date_string, date_format)

        date_string = "1364-6-6 12:13:14"
        dt2 = jdatetime.datetime.strptime(date_string, date_format)

        self.assertEqual(False, dt2 == dt1)

    def test_datetime_eq_now(self):
        import time
        dt1 = jdatetime.datetime.now()
        time.sleep(0.1)
        dt2 = jdatetime.datetime.now()
        self.assertEqual(False, dt2 == dt1)

    def test_timetz(self):
        teh = TehranTime()

        dt_gmt = datetime.datetime(2015, 6, 27, 1, 2, 3, tzinfo=teh)
        self.assertEqual("01:02:03+03:30", dt_gmt.timetz().__str__())

    def test_datetime_eq_diff_tz(self):
        gmt = GMTTime()
        teh = TehranTime()

        dt_gmt = datetime.datetime(2015, 6, 27, 0, 0, 0, tzinfo=gmt)
        dt_teh = datetime.datetime(2015, 6, 27, 3, 30, 0, tzinfo=teh)
        self.assertEqual(True, dt_teh == dt_gmt, "In standrd python datetime, __eq__ considers timezone")

        jdt_gmt = jdatetime.datetime(1389, 2, 17, 0, 0, 0, tzinfo=gmt)

        jdt_teh = jdatetime.datetime(1389, 2, 17, 3, 30, 0, tzinfo=teh)

        self.assertEqual(True, jdt_teh == jdt_gmt)

    def test_datetimes_with_different_locales_are_not_equal(self):
        dt_en = jdatetime.datetime(2018, 4, 15, 0, 0, 0, locale='en_US')
        dt_fa = jdatetime.datetime(2018, 4, 15, 0, 0, 0, locale='fa_IR')
        self.assertNotEqual(dt_en, dt_fa)

    def test_datetimes_with_different_locales_inequality_works(self):
        dt_en = jdatetime.datetime(2018, 4, 15, 0, 0, 0, locale='en_US')
        dt_fa = jdatetime.datetime(2018, 4, 15, 0, 0, 0, locale='fa_IR')
        self.assertTrue(dt_en != dt_fa)

    def test_fromgregorian_accepts_named_argument_of_date_and_locale(self):
        gd = datetime.date(2018, 7, 14)
        jdt = jdatetime.datetime.fromgregorian(date=gd, locale='nl_NL')
        self.assertEqual(jdt.year, 1397)
        self.assertEqual(jdt.month, 4)
        self.assertEqual(jdt.day, 23)
        self.assertEqual(jdt.locale, 'nl_NL')

    def test_fromgregorian_accepts_named_argument_of_datetime_and_locale(self):
        gdt = datetime.datetime(2018, 7, 15, 11, 7, 0)
        jdt = jdatetime.datetime.fromgregorian(datetime=gdt, locale='nl_NL')
        self.assertEqual(jdt.year, 1397)
        self.assertEqual(jdt.month, 4)
        self.assertEqual(jdt.day, 24)
        self.assertEqual(jdt.hour, 11)
        self.assertEqual(jdt.minute, 7)
        self.assertEqual(jdt.locale, 'nl_NL')

    def test_fromgregorian_accepts_named_argument_of_date_with_date_input(self):
        gdt = datetime.date(2018, 7, 15)
        jdt = jdatetime.datetime.fromgregorian(date=gdt, locale='nl_NL')
        self.assertEqual(jdt.year, 1397)
        self.assertEqual(jdt.month, 4)
        self.assertEqual(jdt.day, 24)
        self.assertEqual(jdt.hour, 0)
        self.assertEqual(jdt.minute, 0)
        self.assertEqual(jdt.locale, 'nl_NL')

    def test_fromgregorian_accepts_named_argument_of_date_with_datetime_input(self):
        gdt = datetime.datetime(2018, 7, 15, 11, 7, 0)
        jdt = jdatetime.datetime.fromgregorian(date=gdt, locale='nl_NL')
        self.assertEqual(jdt.year, 1397)
        self.assertEqual(jdt.month, 4)
        self.assertEqual(jdt.day, 24)
        self.assertEqual(jdt.hour, 11)
        self.assertEqual(jdt.minute, 7)
        self.assertEqual(jdt.locale, 'nl_NL')

    def test_fromgregorian_accepts_year_month_day_and_locale(self):
        jdt = jdatetime.datetime.fromgregorian(year=2018, month=7, day=15, locale='nl_NL')
        self.assertEqual(jdt.year, 1397)
        self.assertEqual(jdt.month, 4)
        self.assertEqual(jdt.day, 24)
        self.assertEqual(jdt.locale, 'nl_NL')

    def test_datetime_raise_exception_on_invalid_calculation(self):
        date_1395 = jdatetime.datetime(1395, 1, 1)

        with self.assertRaises(TypeError):
            date_1395 - 1

        with self.assertRaises(TypeError):
            date_1395 + 1

        with self.assertRaises(TypeError):
            jdatetime.timedelta(days=1) - date_1395

        with self.assertRaises(TypeError):
            date_1395 + date_1395

    def test_datetime_calculation_on_timedelta(self):
        date_1395 = jdatetime.datetime(1395, 1, 1)
        day_before = date_1395 - jdatetime.timedelta(days=1)
        day_after = date_1395 + jdatetime.timedelta(days=1)

        self.assertEqual(day_before, jdatetime.datetime(1394, 12, 29, 0, 0))
        self.assertEqual(day_after, jdatetime.datetime(1395, 1, 2, 0, 0))

        day_after = jdatetime.timedelta(days=1) + date_1395

        self.assertEqual(day_before, jdatetime.datetime(1394, 12, 29, 0, 0))
        self.assertEqual(day_after, jdatetime.datetime(1395, 1, 2, 0, 0))

    def test_datetime_calculation_on_two_dates(self):
        date_1394 = jdatetime.datetime(1394, 1, 1)
        date_1395 = jdatetime.datetime(1395, 1, 1)

        day_diff = date_1395 - date_1394

        self.assertEqual(day_diff, datetime.timedelta(365))

        day_diff = date_1394 - date_1395

        self.assertEqual(day_diff, datetime.timedelta(-365))

    def test_date_raise_exception_on_invalid_calculation(self):
        date_1395 = jdatetime.date(1395, 1, 1)

        with self.assertRaises(TypeError):
            date_1395 - 1

        with self.assertRaises(TypeError):
            date_1395 + 1

        with self.assertRaises(TypeError):
            jdatetime.timedelta(days=1) - date_1395

        with self.assertRaises(TypeError):
            date_1395 + date_1395

    def test_date_calculation_on_timedelta(self):
        date_1395 = jdatetime.date(1395, 1, 1)
        day_before = date_1395 - jdatetime.timedelta(days=1)
        day_after = date_1395 + jdatetime.timedelta(days=1)

        self.assertEqual(day_before, jdatetime.date(1394, 12, 29))
        self.assertEqual(day_after, jdatetime.date(1395, 1, 2))

        day_after = jdatetime.timedelta(days=1) + date_1395

        self.assertEqual(day_before, jdatetime.date(1394, 12, 29))
        self.assertEqual(day_after, jdatetime.date(1395, 1, 2))

    def test_date_calculation_on_two_dates(self):
        date_1394 = jdatetime.date(1394, 1, 1)
        date_1395 = jdatetime.date(1395, 1, 1)

        day_diff = date_1395 - date_1394

        self.assertEqual(day_diff, datetime.timedelta(365))

        day_diff = date_1394 - date_1395

        self.assertEqual(day_diff, datetime.timedelta(-365))

    def test_add_timedelta_keeps_source_datetime_locale(self):
        jdate = jdatetime.datetime(1397, 4, 23, locale='nl_NL')
        new_jdate = jdate + datetime.timedelta(days=1)
        self.assertEqual(new_jdate.year, 1397)
        self.assertEqual(new_jdate.month, 4)
        self.assertEqual(new_jdate.day, 24)
        self.assertEqual(new_jdate.locale, 'nl_NL')

    def test_subtract_timedelta_keeps_source_datetime_locale(self):
        jdate = jdatetime.datetime(1397, 4, 23, locale='nl_NL')
        new_jdate = jdate - datetime.timedelta(days=1)
        self.assertEqual(new_jdate.year, 1397)
        self.assertEqual(new_jdate.month, 4)
        self.assertEqual(new_jdate.day, 22)
        self.assertEqual(new_jdate.locale, 'nl_NL')

    def test_with_none_locale_set(self):
        self.reset_locale()
        day_of_week = jdatetime.date(1395, 1, 2).strftime("%a")

        self.assertEqual(day_of_week, "Mon")

    def reset_locale(self):
        if platform.system() == 'Windows':
            locale.setlocale(locale.LC_ALL, 'English_United States')
        else:
            locale.resetlocale()

    def test_with_fa_locale(self):
        self.set_fa_locale()
        day_of_week = jdatetime.date(1395, 1, 2).strftime("%a")

        self.assertEqual(day_of_week, u"دوشنبه")

    def set_fa_locale(self):
        if platform.system() == 'Windows':
            locale.setlocale(locale.LC_ALL, 'Persian')
        else:
            locale.setlocale(locale.LC_ALL, "fa_IR")

    def test_datetime_to_str(self):
        date = jdatetime.datetime(1394, 1, 1, 0, 0, 0)
        self.assertEqual(str(date), "1394-01-01 00:00:00")

    def test_with_pytz(self):
        try:
            import pytz
            from pytz import timezone
        except Exception:
            pytz = None
        if pytz:
            tehran = timezone('Asia/Tehran')
            date = jdatetime.datetime(1394, 1, 1, 0, 0, 0, tzinfo=tehran)
            self.assertEqual(str(date), "1394-01-01 00:00:00+0326")

    def test_as_locale_returns_same_datetime_with_specified_locale(self):
        jdt_en = jdatetime.datetime(1397, 4, 23, 11, 47, 30, 40, locale='en_US')
        jdt_fa = jdt_en.aslocale('fa_IR')
        self.assertEqual(jdt_fa.year, 1397)
        self.assertEqual(jdt_fa.month, 4)
        self.assertEqual(jdt_fa.day, 23)
        self.assertEqual(jdt_fa.hour, 11)
        self.assertEqual(jdt_fa.minute, 47)
        self.assertEqual(jdt_fa.second, 30)
        self.assertEqual(jdt_fa.microsecond, 40)
        self.assertEqual(jdt_fa.locale, 'fa_IR')

    def test_timetuple(self):
        jdt = jdatetime.datetime(1397, 4, 23, 11, 47, 30, 40)
        self.assertEqual(
            jdt.timetuple(),
            time.struct_time((2018, 7, 14, 11, 47, 30, 5, 195, -1)),
        )

    @unittest.skipUnless(
        hasattr(datetime.datetime, 'timestamp'),
        '`datetime.datetime.timestamp` is not implemented in older pythons',
    )
    def test_timestamp_implemented(self):
        teh = TehranTime()
        jdt = jdatetime.datetime(1397, 4, 23, 11, 47, 30, 40, tzinfo=teh)
        self.assertEqual(jdt.timestamp(), 1531556250.00004)

    @unittest.skipIf(
        hasattr(datetime.datetime, 'timestamp'),
        '`datetime.datetime.timestamp` is not implemented in older pythons',
    )
    def test_timestamp_not_implemented(self):
        teh = TehranTime()
        jdt = jdatetime.datetime(1397, 4, 23, 11, 47, 30, 40, tzinfo=teh)
        with self.assertRaises(NotImplementedError):
            jdt.timestamp()

    def test_isoformat_default_args(self):
        jdt = jdatetime.datetime(1398, 4, 11)
        jiso = jdt.isoformat()

        self.assertAlmostEqual(jiso, '1398-04-11T00:00:00')

    def test_isoformat_custom_sep(self):
        jdt = jdatetime.datetime(1398, 4, 11)
        jiso = jdt.isoformat('M')

        self.assertAlmostEqual(jiso, '1398-04-11M00:00:00')

    def test_isoformat_bad_sep(self):
        jdt = jdatetime.datetime(1398, 4, 11)

        for t in ['dummy', 123, 123.123, (1, 2, 3), [1, 2, 3]]:
            with self.assertRaises(AssertionError):
                jdt.isoformat(t)

    def test_isoformat_custom_timespec(self):
        jdt = jdatetime.datetime(1398, 4, 11, 11, 6, 5, 123456)

        hours = jdt.isoformat(timespec='hours')
        minutes = jdt.isoformat(timespec='minutes')
        seconds = jdt.isoformat(timespec='seconds')
        milliseconds = jdt.isoformat(timespec='milliseconds')
        microseconds = jdt.isoformat(timespec='microseconds')

        self.assertEqual(hours, '1398-04-11T11')
        self.assertEqual(minutes, '1398-04-11T11:06')
        self.assertEqual(seconds, '1398-04-11T11:06:05')
        self.assertEqual(milliseconds, '1398-04-11T11:06:05.123')
        self.assertEqual(microseconds, '1398-04-11T11:06:05.123456')

    @unittest.skipIf(zoneinfo is None, "ZoneInfo not supported!")
    def test_zoneinfo_as_timezone(self):
        tzinfo = zoneinfo.ZoneInfo('Asia/Tehran')
        jdt = jdatetime.datetime(1398, 4, 11, 11, 6, 5, 123456, tzinfo=tzinfo)
        self.assertEqual(str(jdt), '1398-04-11 11:06:05.123456+0430')


class TestJdatetimeGetSetLocale(unittest.TestCase):
    @staticmethod
    def record_thread_locale(record, event, locale):
        """Set and capture locale in current thread.
        Use an event to coordinate execution for multithreaded
        tests. Because thread idents maybe recycled and reused
        and jdatetime uses threads idents to identify unique
        threads.
        """
        event.wait(timeout=10)
        jdatetime.set_locale(locale)
        record.append(jdatetime.get_locale())

    def test_get_locale_returns_none_if_no_locale_set_yet(self):
        self.assertIsNone(jdatetime.get_locale())

    @unittest.skipIf(greenlet_installed, 'thread ident is used when greenlet is not installed')
    def test_set_locale_is_per_thread_with_no_effect_on_other_threads(self):
        event = threading.Event()
        fa_record = []
        fa_thread = threading.Thread(target=self.record_thread_locale, args=(fa_record, event, 'fa_IR'))
        nl_record = []
        nl_thread = threading.Thread(target=self.record_thread_locale, args=(nl_record, event, 'nl_NL'))

        fa_thread.start()
        nl_thread.start()
        event.set()  # ensure both threads run concurrently
        fa_thread.join()
        nl_thread.join()

        self.assertEqual(1, len(fa_record))
        self.assertEqual('fa_IR', fa_record[0])
        self.assertEqual(1, len(nl_record))
        self.assertEqual('nl_NL', nl_record[0])
        self.assertIsNone(jdatetime.get_locale())  # MainThread is not affected neither

    @unittest.skipUnless(greenlet_installed, 'greenelts ident is used when greenlet module is installed')
    def test_set_locale_is_per_greenlet_with_no_effect_on_other_greenlets(self):
        fa_record = []

        def record_greenlet_locale_fa():
            jdatetime.set_locale('fa_IR')
            nl_greenlet.switch()
            fa_record.append(jdatetime.get_locale())
            nl_greenlet.switch()

        nl_record = []

        def record_greenlet_locale_nl():
            jdatetime.set_locale('nl_NL')
            fa_greenlet.switch()
            nl_record.append(jdatetime.get_locale())
            fa_greenlet.switch()

        fa_greenlet = greenlet.greenlet(record_greenlet_locale_fa)
        nl_greenlet = greenlet.greenlet(record_greenlet_locale_nl)
        fa_greenlet.switch()

        self.assertEqual(1, len(fa_record))
        self.assertEqual('fa_IR', fa_record[0])
        self.assertEqual(1, len(nl_record))
        self.assertEqual('nl_NL', nl_record[0])

    @unittest.skipIf(greenlet_installed, 'thread ident is used when greenlet is not installed')
    def test_set_locale_sets_default_locale_for_date_objects(self):
        def record_locale_formatted_date(record, locale):
            jdatetime.set_locale(locale)
            dt = jdatetime.date(1397, 3, 27)
            record.append(dt.strftime('%A'))
            record.append(dt.strftime('%B'))

        fa_record = []
        fa_th = threading.Thread(target=record_locale_formatted_date, args=(fa_record, jdatetime.FA_LOCALE))
        fa_th.start()
        fa_th.join()

        self.assertEqual([u'یکشنبه', u'خرداد'], fa_record)

    @unittest.skipUnless(greenlet_installed, 'greenlets ident is used when greenlet module is installed')
    def test_set_locale_sets_default_locale_for_date_objects_with_greenlets(self):
        def record_locale_formatted_date(record, locale):
            jdatetime.set_locale(locale)
            dt = jdatetime.date(1397, 3, 27)
            record.append(dt.strftime('%A'))
            record.append(dt.strftime('%B'))

        fa_record = []
        fa_greenlet = greenlet.greenlet(record_locale_formatted_date)
        fa_greenlet.switch(fa_record, jdatetime.FA_LOCALE)

        self.assertEqual([u'یکشنبه', u'خرداد'], fa_record)


if __name__ == "__main__":
    unittest.main()
