#  The algorithms to convert between Jalali and Gregorian dates, are based on
#  FarsiWeb's jalali.c library (http://www.farsiweb.info/jalali/jalali.c).
# 
#  Copyright (C) 2001  Roozbeh Pournader <roozbeh@sharif.edu>
#  Copyright (C) 2001  Mohammad Toossi <mohammad@bamdad.org>
#  Copyright (C) 2003-2011 Parspooyesh Fanavar (http://parspooyesh.com/)
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You can receive a copy of GNU Lesser General Public License at the
#  World Wide Web address <http://www.gnu.org/licenses/lgpl.html>.

g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
j_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]


class GregorianToJalali:
    def __init__(self, gyear, gmonth, gday):
        """
        Convert gregorian date to jalali date
        gmonth: number of month in range 1-12
        """
        self.gyear = gyear
        self.gmonth = gmonth
        self.gday = gday
        self.__gregorianToJalali()

    def getJalaliList(self):
        return (self.jyear, self.jmonth, self.jday)

    def __gregorianToJalali(self):
        """
        g_y: gregorian year
        g_m: gregorian month
        g_d: gregorian day
        """
        gy = self.gyear - 1600
        gm = self.gmonth - 1

        j_day_no = (
            365 * gy + (gy + 3) // 4 - (gy + 99) // 100
            + (gy + 399) // 400 + self.gday - 1 - 79
        )

        for i in range(gm):
            j_day_no += g_days_in_month[i]
        if gm > 1 and ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
            # leap and after Feb
            j_day_no += 1

        j_np = j_day_no // 12053
        j_day_no %= 12053
        jy = 979 + 33 * j_np + 4 * (j_day_no // 1461)

        j_day_no %= 1461

        if j_day_no >= 366:
            j_day_no -= 1
            jy += j_day_no // 365
            j_day_no %= 365

        for i in range(11):
            if not j_day_no >= j_days_in_month[i]:
                i -= 1
                break
            j_day_no -= j_days_in_month[i]

        self.jyear = jy
        self.jmonth = i + 2
        self.jday = j_day_no + 1


class JalaliToGregorian:
    def __init__(self, jyear, jmonth, jday):
        """
        Convert db time stamp (in gregorian date) to jalali date
        """
        self.jyear = jyear
        self.jmonth = jmonth
        self.jday = jday
        self.__jalaliToGregorian()

    def getGregorianList(self):
        return (self.gyear, self.gmonth, self.gday)

    def __jalaliToGregorian(self):
        jy = self.jyear - 979
        g_day_no = 365 * jy + (jy // 33) * 8 + (jy % 33 + 3) // 4 + self.jday - 1 + 79
        for i in range(self.jmonth - 1):
            g_day_no += j_days_in_month[i]

        gy = 1600 + 400 * (g_day_no // 146097)  # 146097 = 365*400 + 400/4 - 400/100 + 400/400
        g_day_no %= 146097

        leap = 1
        if g_day_no >= 36525:  # 36525 = 365*100 + 100/4
            g_day_no -= 1
            gy += 100 * (g_day_no // 36524)  # 36524 = 365*100 + 100/4 - 100/100
            g_day_no %= 36524

            if g_day_no >= 365:
                g_day_no += 1
            else:
                leap = 0

        gy += 4 * (g_day_no // 1461)  # 1461 = 365*4 + 4/4
        g_day_no %= 1461

        if g_day_no >= 366:
            leap = 0
            g_day_no -= 1
            gy += g_day_no // 365
            g_day_no %= 365

        i = 0
        while g_day_no >= g_days_in_month[i] + (i == 1 and leap):
            g_day_no -= g_days_in_month[i] + (i == 1 and leap)
            i += 1
        self.gmonth = i + 1
        self.gday = g_day_no + 1
        self.gyear = gy
