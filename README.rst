jdatetime
=========
jdatetime is Jalali_ implementation of Python's datetime module

Status
------

.. image:: https://travis-ci.org/slashmili/python-jalali.svg?branch=master
    :target: https://travis-ci.org/slashmili/python-jalali

.. image:: https://img.shields.io/pypi/v/jdatetime.svg
   :target: https://pypi.python.org/pypi/jdatetime

.. image:: https://img.shields.io/pypi/dm/jdatetime.svg

Install
-------
``pip install jdatetime``

Documents
---------
This module exactly follows Python Standard datetime module's methods http://docs.python.org/release/2.7.1/library/datetime.html

Also these methods are addedd to jdatetime.date and jdatetime.datetime :

.. code::

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



Example
-------

.. code:: shell

    $ python
    Python 2.6.6 (r266:84292, Sep 15 2010, 15:52:39)
    [GCC 4.4.5] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> import jdatetime
    >>> jdatetime.datetime.now()
    jdatetime.datetime(1394, 12, 4, 8, 37, 31, 855729)
    >>> jdatetime.date.today()
    jdatetime.date(1394, 12, 4)

Locale
------
In order to get the date string in farsi you need to set the locale to fa_IR

.. code:: shell

    $ python
    Python 2.7.9 (default, Mar  1 2015, 12:57:24)
    [GCC 4.9.2] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> import locale
    >>> import jdatetime
    >> jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
    u'Wed, 08 Ord 1395 20:47:32'
    >>> locale.setlocale(locale.LC_ALL, "fa_IR")
    'fa_IR'
    >>> jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
    u'\u0686\u0647\u0627\u0631\u0634\u0646\u0628\u0647, 08 \u0627\u0631\u062f\u06cc\u0628\u0647\u0634\u062a 1395 20:47:56'

.. _Jalali: http://en.wikipedia.org/wiki/Iranian_calendar
