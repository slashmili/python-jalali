import datetime
from jalali import GregorianToJalali, JalaliToGregorian, j_days_in_month
MINYEAR=1
MAXYEAR=9377

class date(object):
    year  = 0
    month = 0 
    day   = 0
    def __init__(self, year, month, day):
        """date(year, month, day) --> date object"""
        if year < MINYEAR or year >MAXYEAR :
            raise ValueError , "year is out of range"
        if month < 1 or month > 12 :
            raise ValueError, "month must be in 1..12"
        if day< 1 :
            raise ValueError, "day is out of range for month"
        if day > j_days_in_month[month-1] :
            raise ValueError, "day is out of range for month"

        self.year  = year
        self.month = month
        self.day   = day
        pass
    
    #def __getattribute__(self, name):
    #    print name

    @staticmethod
    def today():
        """Current date or datetime:  same as self.__class__.fromtimestamp(time.time())."""
        to = datetime.date.today()
        (y, m, d) = GregorianToJalali(to.year, to.month, to.day).getJalaliList()
        return date(y, m, d)

    @staticmethod
    def fromtimestamp(timestamp):
        d         = datetime.date.fromtimestamp(timestamp)
        (y, m, d) = GregorianToJalali(d.year, d.month, d.day).getJalaliList()
        return date(y, m, d)

    @staticmethod 
    def fromordinal(ordinal):
        """int -> date corresponding to a proleptic Jalali ordinal. 
        it starts from Farvardin 1 of year 1, which is equal to 622-3-21 of Gregorian"""
        if ordinal < 1 :
            raise ValueError, "ordinal must be >= 1"
        d         = datetime.date.fromordinal(226894 +ordinal)
        (y, m, d) =  GregorianToJalali(d.year, d.month, d.day).getJalaliList()
        return date(y, m, d)
    def __repr__(self):
       return  "jdatetime.date(%s, %s, %s)"%(self.year, self.month, self.day)

    def __str__(self):
        return "%s-%s-%s"%(self.year ,self.month ,self.day)
    
    def __add__(self, timedelta):
        """x.__add__(y) <==> x+y"""
        if type(timedelta) != datetime.timedelta :
            raise TypeError, ("unsupported operand type(s) for +: '%s' and '%s'"%(type(self), type(timedelta)))
        (y, m, d) = JalaliToGregorian(self.year, self.month, self.day).getGregorianList()
        gd = datetime.date(y, m, d) + timedelta
        (y, m, d) = GregorianToJalali(gd.year, gd.month, gd.day).getJalaliList()
        return date(y, m, d)

    def __sub__(self, timedelta):
        """x.__sub__(y) <==> x-y"""
        if type(timedelta) != datetime.timedelta :
            raise TypeError, ("unsupported operand type(s) for +: '%s' and '%s'"%(type(self), type(timedelta)))
        (y, m, d) = JalaliToGregorian(self.year, self.month, self.day).getGregorianList()
        gd = datetime.date(y, m, d) - timedelta
        (y, m, d) = GregorianToJalali(gd.year, gd.month, gd.day).getJalaliList()
        return date(y, m, d)

    def __eq__(self, other_date):
        """x.__eq__(y) <==> x==y"""
        if self.year == other_date.year and self.month == other_date.month and self.day == other_date.day :
            return True
        return False

    def __ge__(self, other_date):
        """x.__ge__(y) <==> x>=y"""
        if self.year > other_date.year : 
            return True
        elif self.year == other_date.year :
            if self.month > other_date.month :
                return True
            elif self.month == other_date.month and self.day >= other_date.day :
                return True
        return False

    def __gt__(self, other_date):
        """x.__gt__(y) <==> x>y"""
        if self.year > other_date.year :
            return True
        elif self.year == other_date.year :
            if self.month > other_date.month :
                return True
            elif self.month >= other_date.month and self.day > other_date.day :
                return True
        return False

    def __le__(self, other_date):
        """x.__le__(y) <==> x<=y"""
        return not self.__ge__(other_date)

        if self.year < other_date.year:
            return True
        elif self.year == other_date.year :
            if self.month < other_date.month :
                return True
            elif self.month == other_date.month and self.day <= other_date.day :
                return True
        return False

    def __lt__(self, other_date):
        """x.__lt__(y) <==> x<y"""
        return not self.__gt__(other_date)
        if self.year < other_date.year:
            return True
        elif self.year == other_date.year :
            if self.month < other_date.month :
                return True
            elif self.month == other_date.month and self.day < other_date.day :
                return True
        return False

    def __ne__(self, other_date):
        """x.__ne__(y) <==> x!=y"""
        return not self.__eq__(other_date)
    
    def __radd__(self, timedelta):
        """x.__radd__(y) <==> y+x"""
        return self.__add__(timedelta)

    def __rsub__(self, timedelta):
        """x.__rsub__(y) <==> y-x"""
        return self.__sub__(timedelta)

    def __hash__(self): 
        """x.__hash__() <==> hash(x)"""
        (y, m, d) = JalaliToGregorian(self.year, self.month, self.day).getGregorianList()
        gd = datetime.date(y, m, d) 
        return gd.__hash__()

    def ctime(self):
        """Return ctime() style string."""
        #TODO: elli nagozasht baghiesh ro emsham anjam bedam yadet bashe farda anjam bedi
        #'Mon May  2 00:00:00 2011'

timedelta = datetime.timedelta
