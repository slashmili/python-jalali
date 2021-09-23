jdatetime
=========
jdatetime is Jalali_ implementation of Python's datetime module

Status
------

.. image:: https://github.com/slashmili/python-jalali/workflows/Tests/badge.svg?branch=main
   :target: https://github.com/slashmili/python-jalali/actions


.. image:: https://ci.appveyor.com/api/projects/status/ge5rk703ydx649a6?svg=true
   :target: https://ci.appveyor.com/project/slashmili/python-jalali

.. image:: https://img.shields.io/pypi/v/jdatetime.svg
   :target: https://pypi.python.org/pypi/jdatetime

.. image:: https://img.shields.io/pypi/pyversions/jdatetime.svg
   :target: https://pypi.python.org/pypi/jdatetime

Install
-------
``pip install jdatetime``

Documents
---------
This module exactly follows Python Standard datetime module's methods http://docs.python.org/release/2.7.1/library/datetime.html

Also these methods are added to jdatetime.date and jdatetime.datetime :


.. code-block:: python

    fromgregorian(**kw)
        Convert gregorian to jalali and return jdatetime.date
        jdatetime.date.fromgregorian(day=X,month=X,year=X)
        jdatetime.date.fromgregorian(date=datetime.date)
        jdatetime.datetime.fromgregorian(datetime=datetime.datetime)
    togregorian(self)
        Convert current jalali date to gregorian and return datetime.date
    isleap(self)
        check if year is leap year
        algortim is based on http://en.wikipedia.org/wiki/Leap_year



Example
-------

.. code-block:: shell

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
In order to get the date string in farsi you need to set the locale to fa_IR. The locale
could be specified explicitly upon instantiation of `date`/`datetime` instances, or by
setting a default locale.

Instance locales is *named argument only*:

.. code-block:: python

    import jdatetime
    fa_date = jdatetime.date(1397, 4, 23, locale='fa_IR')
    fa_datetime = jdatetime.datetime(1397, 4, 23, 11, 40, 30, locale='fa_IR')


`date` and `datetime` instances provide the method `aslocale()` to return a clone of the instance
with the same timestamp, in a different locale.


Default Locale
~~~~~~~~~~~~~~
It's possible to set the default locale, so all new instances created afterwards would use
the desired locale, unless explicitly specified otherwise.

.. code-block:: shell

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


If your requirements demand to support different locales withing the same process,
you could set the default locale per thread. New `date` and `datetime` instances
created in each thread, will use the specified locale by default.
This supports both Python threads, and greenlets.


.. code-block:: python

    import jdatetime
    jdatetime.set_locale('fa_IR')
    jdatetime.datetime.now().strftime('%A %B')
    # u'\u062f\u0648\u0634\u0646\u0628\u0647 \u062e\u0631\u062f\u0627\u062f'

Release Steps
~~~~~~~~~~~~~~
* Bump the version setup.py
* Add release notes in CHANGELOG.md
* Commit and create a tag with a name like v3.5.9
* python setup.py sdist bdist_wheel
* twine upload --repository testpypi dist/jdatetime-3.5.9.tar.gz
* verify the version in testpypi: https://test.pypi.org/project/jdatetime/
* twine upload dist/jdatetime-3.5.9.tar.gz
* verify the version in pypi: https://pypi.org/project/jdatetime/

.. _Jalali: http://en.wikipedia.org/wiki/Iranian_calendar
