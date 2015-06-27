jdatetime
=========
jdatetime is [Jalali](http://en.wikipedia.org/wiki/Iranian_calendar) implementation of Python's datetime module


[![Build Status](https://travis-ci.org/slashmili/python-jalali.svg?branch=master)](https://travis-ci.org/slashmili/python-jalali)


INSTALL
-------
Install it with easy_install
```
easy_install jdatetime
```
OR install it from source
```
python setup.py install
```

Documents
---------
This module exactly follows Python Standard [datetime module's methods](http://docs.python.org/release/2.7.1/library/datetime.html)

Also these methods are addedd to jdatetime.date and jdatetime.datetime :
```
 |  fromgregorian(**kw)
 |      Convert gregorian to jalali and return jdatetime.date
 |      jdatetime.date.fromgregorian(day=X,month=X,year=X)
 |      jdatetime.date.fromgregorian(date=datetime.date)
 |      jdatetime.date.fromgregorian(datetime=datetime.datetime)
 |  togregorian(self)
 |      Convert current jalali date to gregorian and return datetime.date
 |  isleap(self)
 |      check if year is leap year
 |      algortim is based on http://en.wikipedia.org/wiki/Leap_year
 ```

