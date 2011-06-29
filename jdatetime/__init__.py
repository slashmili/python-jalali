import datetime as py_datetime
from jalali import GregorianToJalali, JalaliToGregorian, j_days_in_month
MINYEAR=1
MAXYEAR=9377

timedelta = py_datetime.timedelta

class time(py_datetime.time):
    def __repr__(self):
       return  "jdatetime.time(%s, %s, %s)"%(self.hour, self.minute, self.second)


class date(object):
    """date(year, month, day) --> date object"""
    j_months       = ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar', 
               'Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand']
    j_months_short = ['Far', 'Ord', 'Kho', 'Tir', 'Mor', 'Sha', 
               'Meh', 'Aba', 'Aza', 'Dey', 'Bah', 'Esf']

    j_weekdays       = ['Shanbeh', 'Yekshanbeh','Doshanbeh', 
                  'SehShanbeh', 'Chaharshanbeh', 'Panjshanbeh','Jomeh']
    j_weekdays_short = ['Sha', 'Yek','Dos', 
                  'Seh', 'Cha', 'Pan','Jom']


    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month

    @property
    def day(self):
        return self.__day

    __year  = 0
    __month = 0
    __day   = 0

    def __check_arg(self,value):
       if type(value) is int or type(value) is long :
           return True
       return False


    def __init__(self, year, month, day):
        """date(year, month, day) --> date object"""
        if not (self.__check_arg(year) and self.__check_arg(month) and self.__check_arg(day)) :
            raise TypeError, "an integer is required"
        if year < MINYEAR or year >MAXYEAR :
            raise ValueError , "year is out of range"
        if month < 1 or month > 12 :
            raise ValueError, "month must be in 1..12"
        if day< 1 :
            raise ValueError, "day is out of range for month"
        if month == 12 and day == 30 and self.isleap:
            #Do nothing
            pass
        elif day > j_days_in_month[month-1] :
            raise ValueError, "day is out of range for month"

        self.__year  = year
        self.__month = month
        self.__day   = day
        pass
    
    
    """The smallest possible difference between non-equal date objects, timedelta(days=1)."""
    resolution = timedelta(1) 

    """The earliest representable date, date(MINYEAR, 1, 1)"""
    #min = date(MINYEAR, 1, 1)
    #TODO fixed errror :  name 'date' is not defined
    """The latest representable date, date(MAXYEAR, 12, 31)."""
    #max = date(MAXYEAR, 12,29)

    def isleap(self):
        """check if year is leap year
            algortim is based on http://en.wikipedia.org/wiki/Leap_year"""
        return self.year % 33 in (1, 5, 9, 13, 17, 22, 26, 30)

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
        if other_date == None :
            return False
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
        if other_date == None:
            return True
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

    def isoformat(self):
        """Return a string representing the date in ISO 8601 format, 'YYYY-MM-DD'"""
        return self.strftime("%Y-%m-%d")

    #TODO: create jtime !
    #def timetuple(self):
    #    pass
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

        #TODO: fix AM, PM
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

class datetime(object):
    __date = None
    __time = None

    def time(self):
        """Return time object with same time but with tzinfo=None."""
        return self.__time

    def date(self):
        """Return date object with same year, month and day."""
        return self.__date

    def __check_arg(self,value):
       if type(value) is int or type(value) is long :
           return True
       return False

    def __init__(self,year, month, day, hour=None, minute=None, second=None, microsecond=None, tzinfo=None):
        self.__date = date(year, month, day)
       
        tmp_hour = 0
        tmp_min  = 0
        tmp_sec  = 0
        tmp_micr = 0
        if hour != None:
            tmp_hour = hour
        if minute != None:
            tmp_min = minute
        if second !=None :
            tmp_sec = second
        if microsecond !=None:
            tmp_micr = microsecond

        if not (self.__check_arg(tmp_hour) and self.__check_arg(tmp_min) and self.__check_arg(tmp_sec) and self.__check_arg(tmp_micr)) :
            raise TypeError, "an integer is required"
        
        self.__time = time(tmp_hour,tmp_min, tmp_sec, tmp_micr,tzinfo) 

    def __repr__(self):
        if self.__time.tzinfo != None :
            return  "jdatetime.datetime(%s, %s, %s, %s, %s, %s, %s, tzinfo=%s)"%(self.__date.year, self.__date.month, self.__date.day,self.__time.hour, self.__time.minute, self.__time.second, self.__time.microsecond ,self.__time.tzinfo)
        
        if self.__time.microsecond != 0 :
            return  "jdatetime.datetime(%s, %s, %s, %s, %s, %s, %s)"%(self.__date.year, self.__date.month, self.__date.day,self.__time.hour, self.__time.minute, self.__time.second, self.__time.microsecond)

        if self.__time.second != 0 :
            return  "jdatetime.datetime(%s, %s, %s, %s, %s, %s)"%(self.__date.year, self.__date.month, self.__date.day,self.__time.hour, self.__time.minute, self.__time.second)

        return  "jdatetime.datetime(%s, %s, %s, %s, %s)"%(self.__date.year, self.__date.month, self.__date.day,self.__time.hour, self.__time.minute)
    
    @staticmethod
    def today():
        """Current date or datetime"""
        return datetime.now()

    @staticmethod
    def now(tz=None):
        """[tz] -> new datetime with tz's local day and time."""
        now_datetime = py_datetime.datetime.now(tz)
        now = date.fromgregorian(date=now_datetime.date())
        return datetime(now.year, now.month, now.day, now_datetime.hour, now_datetime.minute, now_datetime.second, now_datetime.microsecond, tz)

    @staticmethod
    def utcnow():
        """Return a new datetime representing UTC day and time."""
        now_datetime = py_datetime.datetime.utcnow()
        now = date.fromgregorian(date=now_datetime.date())
        return datetime(now.year, now.month, now.day, now_datetime.hour, now_datetime.minute, now_datetime.second, now_datetime.microsecond)
        
    @staticmethod
    def fromtimestamp(timestamp, tz=None):
        """timestamp[, tz] -> tz's local time from POSIX timestamp."""
        now_datetime = py_datetime.datetime.fromtimestamp(timestamp, tz)
        now = date.fromgregorian(date=now_datetime.date())
        return datetime(now.year, now.month, now.day, now_datetime.hour, now_datetime.minute, now_datetime.second, now_datetime.microsecond, tz)

    @staticmethod
    def utcfromtimestamp(timestamp):
        """timestamp -> UTC datetime from a POSIX timestamp (like time.time())."""
        now_datetime = py_datetime.datetime.fromtimestamp(timestamp)
        now = date.fromgregorian(date=now_datetime.date())
        return datetime(now.year, now.month, now.day, now_datetime.hour, now_datetime.minute, now_datetime.second, now_datetime.microsecond)

    @staticmethod
    def combine(d=None, t=None, **kw):
        """date, time -> datetime with same date and time fields"""

        c_date = None
        if d != None :
            c_date = d
        elif 'date' in kw :
            c_date = kw['date']

        c_time = None
        if t != None:
            c_time = t
        elif 'time' in kw :
            c_time = kw['time']

        if c_date == None :
            raise TypeError , "Required argument 'date' (pos 1) not found"
        if c_time == None :
            raise TypeError , "Required argument 'date' (pos 2) not found"

        if type(c_date) != date :
            raise TypeError, "combine() argument 1 must be jdatetime.date, not %s"%(type(c_date))
        if type(c_time) != time :
            raise TypeError, "combine() argument 2 must be jdatetime.time, not %s"%(type(c_time))
        
        return datetime(c_date.year, c_date.month, c_date.day, c_time.hour, c_time.minute, c_time.second, c_time.microsecond, c_time.tzinfo)

    @staticmethod 
    def fromordinal(ordinal):
        """int -> date corresponding to a proleptic Jalali ordinal. 
        it starts from Farvardin 1 of year 1, which is equal to 622-3-21 of Gregorian"""
        if ordinal < 1 :
            raise ValueError, "ordinal must be >= 1"
        d      = py_datetime.date.fromordinal(226894 +ordinal)
        j_date = date.fromgregorian(date=d)
        return datetime(j_date.year, j_date.month, j_date.day, 0, 0)

    @property
    def year(self):
        return self.__date.year

    @property
    def month(self):
        return self.__date.month

    @property
    def day(self):
        return self.__date.day

    @property
    def hour(self):
        return self.__time.day

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
        if '*' in format :
            format = format.replace("*", "\*")
        if '+' in format :
            format = format.replace("+", "\+")
        if '(' in format or ')' in format :
            format = format.replace("(", "\(")
            format = format.replace(")", "\)")
        if '[' in format or ']' in format :
            format = format.replace("[", "\[")
            format = format.replace("]", "\]")
        result_date = {'day': 1, 'month': 1, 'year': 1279, 'microsecond': 0, 'second': 0, 'minute' : 0, 'hour': 0}
        format_map = {
                        '%a': ['[A-Za-z]{3}' , 'day'],
                        '%A': ['[A-Za-z]+'   , 'day'],
                        '%b': ['[A-Za-z]{3}' , 'month'],
                        '%B': ['[A-Za-z]+'   , 'month'],
                        '%d': ['[0-9]{2}'    , 'day'],
                        '%f': ['[0-9]{1,6}'  , 'microsecond'],
                        '%H': ['[0-9]{1,2}'  , 'hour'],
                        '%I': ['[0-9]{1,2}'  , 'hour'],
                        '%j': ['[0-9]{1,3}'  , 'day'],
                        '%m': ['[0-9]{1,2}'  , 'month'],
                        '%M': ['[0-9]{1,2}'  , 'minute'],
                        '%p': ['(AM|PM)'     , 'hour'],
                        '%S': ['[0-9]{1,2}'  , 'second'],
                      }
