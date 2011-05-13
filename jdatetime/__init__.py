import datetime as py_datetime
from jalali import GregorianToJalali, JalaliToGregorian, j_days_in_month
MINYEAR=1
MAXYEAR=9377

timedelta = py_datetime.timedelta
datetime  = py_datetime.datetime

class date(object):
    j_months       = ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar', 
               'Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand']
    j_months_short = ['Far', 'Ord', 'Kho', 'Tir', 'Mor', 'Sha', 
               'Meh', 'Aba', 'Aza', 'Dey', 'Bah', 'Esf']

    j_weekdays       = ['Shanbeh', 'Yekshanbeh','Doshanbeh', 
                  'SehShanbeh', 'Chaharshanbeh', 'Panjshanbeh','Jomeh']
    j_weekdays_short = ['Sha', 'Yek','Dos', 
                  'Seh', 'Cha', 'Pan','Jom']

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
        #TODO: check if it's Kabise allow 30 days
        if day > j_days_in_month[month-1] :
            raise ValueError, "day is out of range for month"

        self.year  = year
        self.month = month
        self.day   = day
        pass
    
    #def __getattribute__(self, name):
    #    print name
    
    """The smallest possible difference between non-equal date objects, timedelta(days=1)."""
    resolution = timedelta(1) 

    """The earliest representable date, date(MINYEAR, 1, 1)"""
    #min = date(MINYEAR, 1, 1)
    #TODO fixed errror :  name 'date' is not defined
    """The latest representable date, date(MAXYEAR, 12, 31)."""
    #max = date(MAXYEAR, 12,29)

    def togregorian(self):
        """Convert current jalali date to gregorian and return datetime.date"""
        (y, m, d) = JalaliToGregorian(self.year, self.month, self.day).getGregorianList()
        return py_datetime.date(y, m, d)

    @staticmethod
    def fromgregorian(**kw):
        """Convert gregorian to jalali and return jdatetime.date
        jdatetime.date.fromgregorian(day=X,month=X,year=X)
        jdatetime.date.fromgregorian(date=datetime.date)
        """
        if 'date' in kw  and type(kw['date']) == py_datetime.date :
            d = kw['date']
            (y, m, d) = GregorianToJalali(d.year, d.month, d.day).getJalaliList()
            return date(y, m, d)
        if 'day' in kw and 'month' in kw and 'year' in kw :
            (year, month, day) = (kw['year'], kw['month'], kw['day'])
            (y, m, d) = GregorianToJalali(year, month, day).getJalaliList()
            return date(y, m, d)

        raise ValueError, "fromgregorian have to called fromgregorian(day=X,month=X,year=X) or fromgregorian(date=datetime.date)"

    @staticmethod
    def today():
        """Current date or datetime:  same as self.__class__.fromtimestamp(time.time())."""
        to = py_datetime.date.today()
        (y, m, d) = GregorianToJalali(to.year, to.month, to.day).getJalaliList()
        return date(y, m, d)

    @staticmethod
    def fromtimestamp(timestamp):
        d         = py_datetime.date.fromtimestamp(timestamp)
        (y, m, d) = GregorianToJalali(d.year, d.month, d.day).getJalaliList()
        return date(y, m, d)

    @staticmethod 
    def fromordinal(ordinal):
        """int -> date corresponding to a proleptic Jalali ordinal. 
        it starts from Farvardin 1 of year 1, which is equal to 622-3-21 of Gregorian"""
        if ordinal < 1 :
            raise ValueError, "ordinal must be >= 1"
        d         = py_datetime.date.fromordinal(226894 +ordinal)
        (y, m, d) =  GregorianToJalali(d.year, d.month, d.day).getJalaliList()
        return date(y, m, d)

    def __repr__(self):
       return  "jdatetime.date(%s, %s, %s)"%(self.year, self.month, self.day)

    def __str__(self):
        return "%s-%s-%s"%(self.year ,self.month ,self.day)
    
    def __add__(self, timedelta):
        """x.__add__(y) <==> x+y"""
        if type(timedelta) != py_datetime.timedelta :
            raise TypeError, ("unsupported operand type(s) for +: '%s' and '%s'"%(type(self), type(timedelta)))
        (y, m, d) = JalaliToGregorian(self.year, self.month, self.day).getGregorianList()
        gd = py_datetime.date(y, m, d) + timedelta
        (y, m, d) = GregorianToJalali(gd.year, gd.month, gd.day).getJalaliList()
        return date(y, m, d)

    def __sub__(self, timedelta):
        """x.__sub__(y) <==> x-y"""
        if type(timedelta) != py_datetime.timedelta :
            raise TypeError, ("unsupported operand type(s) for +: '%s' and '%s'"%(type(self), type(timedelta)))
        (y, m, d) = JalaliToGregorian(self.year, self.month, self.day).getGregorianList()
        gd = py_datetime.date(y, m, d) - timedelta
        (y, m, d) = GregorianToJalali(gd.year, gd.month, gd.day).getJalaliList()
        return date(y, m, d)

    def __eq__(self, other_date):
        """x.__eq__(y) <==> x==y"""
        if type(other_date) != date :
            raise TypeError, ("unsupported operand type for ==: '%s'"%(type(other_date)))
        if self.year == other_date.year and self.month == other_date.month and self.day == other_date.day :
            return True
        return False

    def __ge__(self, other_date):
        """x.__ge__(y) <==> x>=y"""
        if type(other_date) != date :
            raise TypeError, ("unsupported operand type for ==: '%s'"%(type(other_date)))

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
        if type(other_date) != date :
            raise TypeError, ("unsupported operand type for ==: '%s'"%(type(other_date)))

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
        if type(other_date) != date :
            raise TypeError, ("unsupported operand type for ==: '%s'"%(type(other_date)))

        return not self.__ge__(other_date)

    def __lt__(self, other_date):
        """x.__lt__(y) <==> x<y"""
        if type(other_date) != date :
            raise TypeError, ("unsupported operand type for ==: '%s'"%(type(other_date)))

        return not self.__gt__(other_date)

    def __ne__(self, other_date):
        """x.__ne__(y) <==> x!=y"""
        if type(other_date) != date :
            raise TypeError, ("unsupported operand type for ==: '%s'"%(type(other_date)))

        return not self.__eq__(other_date)
    
    def __radd__(self, timedelta):
        """x.__radd__(y) <==> y+x"""
        if type(timedelta) != py_datetime.timedelta :
            raise TypeError, ("unsupported operand type for ==: '%s'"%(type(other_date)))

        return self.__add__(timedelta)

    def __rsub__(self, timedelta):
        """x.__rsub__(y) <==> y-x"""
        if type(timedelta) != py_datetime.timedelta :
            raise TypeError, ("unsupported operand type for ==: '%s'"%(type(other_date)))

        return self.__sub__(timedelta)

    def __hash__(self): 
        """x.__hash__() <==> hash(x)"""
        (y, m, d) = JalaliToGregorian(self.year, self.month, self.day).getGregorianList()
        gd = py_datetime.date(y, m, d) 
        return gd.__hash__()

    def ctime(self):
        """Return ctime() style string."""
        return self.strftime("%c")

    def replace(self, year=0, month=0, day=0):
        """Return date with new specified fields."""
        new_year  = self.year
        new_month = self.month
        new_day   = self.day

        if year != 0 :
            new_year = year
        if month != 0 : 
            new_month = month
        if day != 0 :
            new_day = day

        return date(new_year, new_month, new_day)
    
    def yday(self):
        """return day of year"""
        day = 0
        for i in range(0,self.month - 1):
            day = day + j_days_in_month[i]
        day = day + self.day 
        return day

    def weekday(self):
        """Return the day of the week represented by the date.
        Shanbeh == 0 ... Jomeh == 6"""
        (y, m, d) = JalaliToGregorian(self.year, self.month, self.day).getGregorianList()
        gd = py_datetime.date(y, m, d) 
        if gd.weekday() == 5 :
            return 0
        if gd.weekday() == 6 :
            return 1
        if gd.weekday() == 0 :
            return 2
        if gd.weekday() == 1 :
            return 3
        if gd.weekday() == 2 :
            return 4 
        if gd.weekday() == 3 :
            return 5 
        if gd.weekday() == 4 :
            return 6

    def isoweekday(self):
        """Return the day of the week as an integer, where Shanbeh is 1 and Jomeh is 7"""
        return self.weekday() + 1 


    def weeknumber(self):
        """Return week number """
        return self.yday() / 7 

    def isocalendar(self):
        """Return a 3-tuple, (ISO year, ISO week number, ISO weekday)."""
        return (self.year, self.weeknumber(), self.isoweekday())

    def strftime(self, format):
        """format -> strftime() style string."""
        #TODO: change stupid str.replace 
        #formats = {
        #           '%a': lambda : self.j_weekdays_short[self.weekday()]
        #}
        #find all %[a-zA-Z] and call method if it in formats
        format = format.replace("%a", self.j_weekdays_short[self.weekday()])

        format = format.replace("%A", self.j_weekdays[self.weekday()])


        format = format.replace("%b", self.j_months_short[self.month - 1 ])

        format = format.replace("%B", self.j_months[self.month -1 ])
        #TODO: FIX %d and hardcode hour
        if '%c' in format : 
            format = format.replace("%c", self.strftime("%a %b %d %H:%I:%S %Y"))

        format = format.replace("%d", '%02.d'%(self.day) )
        #TODO: FIXME !
        format = format.replace("%f", str(self.day) )
        #TODO: FIXME !
        format = format.replace("%H", '00' )
        #TODO: FIXME !
        format = format.replace("%I", '00' )
    
        format = format.replace("%j", '%03.d'%( self.yday()) )

        format = format.replace("%m", '%02.d'%( self.month) )

        format = format.replace("%M", '00')

        format = format.replace("%p", 'AM')

        format = format.replace("%S", '00')

        format = format.replace("%w", str(self.weekday()))

        format = format.replace("%W", str(self.weeknumber()))

        if '%x' in format :
            format = format.replace("%x", self.strftime("%m/%d/%y"))

        if '%X' in format :
            format = format.replace("%X", self.strftime('%H:%I:%S'))

        format = format.replace("%Y", str(self.year) )

        format = format.replace("%y", str(self.year)[2:] )

        format = format.replace("%Y", str(self.year) )

        format = format.replace("%z", '')

        format = format.replace("%Z", '')

        return format
