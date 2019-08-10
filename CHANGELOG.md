# Changelog

## [3.5.0] - 2019-08-04
## Add
* Adds support for '%-I' format token
### Fixed
* Fixes '12:mm:ss am' display problem in strftime
* Fixes '%X' token in strftime:
* Fixes Week of year, currently it starts with zero and increases every 7 days, ignoring weekdays

## [3.4.0] - 2019-07-16
### Add
* support subtraction with python datetime

## [3.3.0] - 2019-07-13
### Add
* add isoformat for jdatetime.datetime

## [3.2.0] - 2019-02-02
### Add
* add timetuple and timestamp function

## [3.1.0] - 2018-12-25
### Fixed
* Handle naive datatime in replace function

## [3.0.2] - 2018-09-2
### Fixed
* Handle joint alphabetic characters in strptime format

## [3.0.0] - 2018-07-22
### Add
* Added instance "locale" attribute #37
### Change
* date/datetime instances with different locale attrs are not equal anymore #37
###  Fixed
* fixed a bug in %p placeholder #40

## [2.2.0] - 2018-07-07
### Add
* Added padding-less variations of strftime format symbols #36

## [2.1.0] - 2018-06-20
### Add
* Set default date/datetime locales per thread #35

## [2.0.0] - 2018-02-25
### Add
* Support for pytz


The CHANGELOG for [1.X](https://github.com/slashmili/python-jalali/tree/v1.9.1) releases
