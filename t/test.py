import unittest
import jdatetime
import datetime
import time
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

        dtg = jdatetime.datetime(1380, 12, 1, 1, 2, 4)
        self.assertEqual(True, dtg < dtg + jdatetime.timedelta(seconds=1))
        self.assertEqual(True, dtg - jdatetime.timedelta(seconds=1) < dtg)
        self.assertEqual(False, dtg == None)

    def test_dateconversion(self):
        sample = jdatetime.date(1389,9,2)

        d_check_with = jdatetime.date(1390,2,23)
        #TEST date
        self.assertEqual(True, sample.togregorian() == datetime.date(2010,11,23) )
        self.assertEqual(True, jdatetime.date.fromgregorian(date=datetime.date(2011,5,13)) == d_check_with)

        #TEST datetime
        self.assertEqual(True, jdatetime.datetime.fromgregorian(datetime=datetime.datetime(2011, 5, 13)).date() == d_check_with)

        jd_datetime = jdatetime.datetime.fromgregorian(year=2011, month=5, day=13, hour=14, minute=15, second=16)
        self.assertEqual(True, jd_datetime == jdatetime.datetime.combine(d_check_with, jdatetime.time(14, 15, 16))) 

        gdatetime = datetime.datetime(2011, 5, 13, 14, 15, 16)
        self.assertEqual(True, jd_datetime.togregorian() == gdatetime)

    def test_strftime(self):
        s = jdatetime.date(1390,2,23)
        self.assertEqual(True, s.strftime("%a %A %b %B %c %d %H %I %j %m %M %p %S %w %W %x %X %y %Y %f %z %Z") == 'Jom Jomeh Ord Ordibehesht Jom Ord 23 00:00:00 1390 23 00 00 054 02 00 AM 00 6 7 02/23/90 00:00:00 90 1390 000000  ')


        dt = jdatetime.datetime(1390,2,23, 12, 13, 14, 1)
        self.assertEqual(True, dt.strftime("%a %A %b %B %c %d %H %I %j %m %M %p %S %w %W %x %X %y %Y %f") == 'Jom Jomeh Ord Ordibehesht Jom Ord 23 12:13:14 1390 23 12 12 054 02 13 AM 14 6 7 02/23/90 12:12:14 90 1390 000001')

        class NYCTime(jdatetime.tzinfo):
            def utcoffset(self,dt):
                return jdatetime.timedelta(hours=-4)
            def tzname(self,dt):
                return "EDT"
            def dst(self,dt): 
                return jdatetime.timedelta(0)
        nyc=NYCTime() 
        dt = jdatetime.datetime(1389,2,17,19,10,2,tzinfo=nyc)
        self.assertEqual(True, dt.strftime("%Z %z") == "EDT -0400")

        class TehranTime(jdatetime.tzinfo):
            def utcoffset(self,dt):
                return jdatetime.timedelta(hours=3, minutes=30)
            def tzname(self,dt):
                return "IRDT"
            def dst(self,dt): 
                return jdatetime.timedelta(0)
        teh=TehranTime()
        dt = jdatetime.datetime(1389,2,17,19,10,2,tzinfo=teh)
        self.assertEqual(True, dt.strftime("%Z %z") == "IRDT +0330")

    def test_kabiseh(self):
        kabiseh_year = jdatetime.date.fromgregorian(date=datetime.date(2013,3,20))
        self.assertEqual(True, kabiseh_year.isleap() == True)

        normal_year = jdatetime.date.fromgregorian(date=datetime.date(2014,3,20))
        self.assertEqual(True, normal_year.isleap() == False)

    def test_datetime(self):
        d = jdatetime.datetime(1390, 1, 2, 12, 13, 14)

        self.assertEqual(True, d.time() == jdatetime.time(12, 13, 14))
        self.assertEqual(True, d.date() == jdatetime.date(1390, 1, 2))
        
    def test_datetimetoday(self):
        jnow = jdatetime.datetime.today()
        gnow = jdatetime.date.fromgregorian(date=datetime.datetime.today().date())
        
        self.assertEqual(True, jnow.date() == gnow)

    def test_datetimefromtimestamp(self):
        t = time.time()
        jnow = jdatetime.datetime.fromtimestamp(t).date()
        gnow = datetime.datetime.fromtimestamp(t).date()

        self.assertEqual(True, jdatetime.date.fromgregorian(date=gnow) == jnow)


    def test_combine(self):
        t  = jdatetime.time(12,13,14)
        d  = jdatetime.date(1390, 4, 5)
        dt = jdatetime.datetime(1390, 4, 5, 12, 13, 14)

        self.assertEqual(True, jdatetime.datetime.combine(d,t) == dt)

    def test_replace(self):
        dt  = jdatetime.datetime.today()
        dtr = dt.replace(year=1390, month=12, day=1, hour=13, minute=14, second=15, microsecond = 1233)
        dtn = jdatetime.datetime(1390, 12, 1, 13, 14, 15, 1233)
        
        self.assertEqual(True, dtr == dtn )
    
    def test_strptime(self):
        dt1 = jdatetime.datetime.strptime("1363-6-6 12:13:14","%Y-%m-%d %H:%M:%S")
        dt2 = jdatetime.datetime(1363, 6 , 6 , 12, 13, 14)

        self.assertEqual(True, dt1 == dt2)
unittest.main()
