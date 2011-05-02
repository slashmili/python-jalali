import unittest
import jdatetime

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

unittest.main()
