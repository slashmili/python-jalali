import unittest
import jdatetime
import datetime
class TestJDateTime(unittest.TestCase):
    def test_today(self):
        today = jdatetime.date.today()
        self.assertEqual(1390,today.year)
    
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
        self.assertEqual(False, today < today - jdatetime.timedelta(days=76) )
        self.assertEqual(False, today <= today - jdatetime.timedelta(days=1) )
        self.assertEqual(True, today + jdatetime.timedelta(days=1) >  today  )
        self.assertEqual(True, today + jdatetime.timedelta(days=30) >= today )
        self.assertEqual(True, today == today)
        self.assertEqual(True, today != (jdatetime.date( today.year, today.month, today.day ) + jdatetime.timedelta(days=1) ) )

    def test_dateconversion(self):
        sample = jdatetime.date(1389,9,2)
        self.assertEqual(True, sample.togregorian() == datetime.date(2010,11,23) )
        self.assertEqual(True, jdatetime.date.fromgregorian(date=datetime.date(2011,5,13)) == jdatetime.date(1390,2,23))

    def test_strftime(self):
        s = jdatetime.date(1390,2,23)
        self.assertEqual(True, s.strftime("%a %A %b %B %c %d %f %H %I %j %m %M %p %S %w %W %x %X %y %Y %z %Z") == 'Jom Jomeh Ord Ordibehesht Jom Ord 23 00:00:00 1390 23 23 00 00 054 02 00 AM 00 6 7 02/23/90 00:00:00 90 1390  ')

    def test_kabiseh(self):
        kabiseh_year = jdatetime.date.fromgregorian(date=datetime.date(2013,3,20))
        self.assertEqual(True, kabiseh_year.isleap() == True)

        normal_year = jdatetime.date.fromgregorian(date=datetime.date(2014,3,20))
        self.assertEqual(True, normal_year.isleap() == False)

unittest.main()
