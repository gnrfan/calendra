# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import date
from .core import WesternCalendar, ChristianMixin, Calendar
from .core import SUN, MON, SAT


class Canada(WesternCalendar, ChristianMixin):
    "Canada"
    FIXED_HOLIDAYS = WesternCalendar.FIXED_HOLIDAYS + (
        (7, 1, "Canada Day"),
    )
    shift_new_years_day = True

    def get_variable_days(self, year):
        # usual variable days
        days = super(Canada, self).get_variable_days(year)
        days += [
            (Canada.get_nth_weekday_in_month(year, 9, MON, 1), "Labor Day")
        ]
        canadaday = date(year, 7, 1)
        if canadaday.weekday() in self.get_weekend_days():
            shift = self.find_following_working_day(canadaday)
            days.append((shift, "Canada Day Shift"))
        christmas = date(year, 12, 25)
        if christmas.weekday() in self.get_weekend_days():
            shift = self.find_following_working_day(christmas)
            days.append((shift, "Christmas Shift"))
        return days


class EarlyFamilyDayMixin(Calendar):
    "2nd Monday of February"

    def get_family_day(self, year, label="Family Day"):
        return (self.get_nth_weekday_in_month(year, 2, MON, 2), label)


class LateFamilyDayMixin(Calendar):
    "3rd Monday of February"

    def get_family_day(self, year, label="Family Day"):
        return (self.get_nth_weekday_in_month(year, 2, MON, 3), label)


class VictoriaDayMixin(Calendar):
    "Monday preceding the 25th of May"

    def get_victoria_day(self, year):
        for day in range(18, 25):
            if date(year, 5, day).weekday() == MON:
                return (date(year, 5, day), "Victoria Day")


class AugustCivicHolidayMixin(Calendar):
    "1st Monday of August; different names depending on location"

    def get_civic_holiday(self, year, label="Civic Holiday"):
        return (self.get_nth_weekday_in_month(year, 8, MON),
                label)


class ThanksgivingMixin(Calendar):
    "2nd Monday of October"

    def get_thanksgiving(self, year):
        return (self.get_nth_weekday_in_month(year, 10, MON, 2),
                "Thanksgiving")


class BoxingDayMixin(Calendar):
    "26th of December; shift to next working day"

    def get_boxing_day(self, year):
        boxingday = date(year, 12, 26)
        if boxingday.weekday() == MON:
            days = [(boxingday, "Boxing Day"), (date(year, 12, 27),
                    "Boxing Day (Shift)")]
        elif boxingday.weekday() == SAT or boxingday.weekday() == SUN:
            days = [(boxingday, "Boxing Day"), (date(year, 12, 28),
                    "Boxing Day (Shift)")]
        else:
            days = [(boxingday, "Boxing Day")]
        return days


class StJeanBaptisteMixin(Calendar):
    "24th of June; shift to next working day"

    def get_st_jean(self, year):
        stjean = date(year, 6, 24)
        if stjean.weekday() in self.get_weekend_days():
            days = [(stjean, "St Jean Baptiste"),
                    (self.find_following_working_day(stjean),
                     "St Jean Baptiste (Shift)")]
        else:
            days = [(stjean, "St Jean Baptiste")]
        return days


class RemembranceDayShiftMixin(Calendar):
    "11th of November; shift to next day"
    def get_remembrance_day(self, year):
        remembranceday = date(year, 11, 11)
        if remembranceday.weekday() in self.get_weekend_days():
            days = [(remembranceday, "Remembrance Day"),
                    (self.find_following_working_day(remembranceday),
                    "Remembrance Day (Shift)")]
        else:
            days = [(remembranceday, "Remembrance Day")]
        return days


class Ontario(Canada, BoxingDayMixin, ThanksgivingMixin, VictoriaDayMixin,
              LateFamilyDayMixin, AugustCivicHolidayMixin):
    "Ontario"
    include_good_friday = True

    def get_variable_days(self, year):
        days = super(Ontario, self).get_variable_days(year)
        days += [
            (self.get_family_day(year)),
            (self.get_victoria_day(year)),
            (self.get_civic_holiday(year, "Civic Holiday (Not for all)")),
            (self.get_thanksgiving(year)),
        ]
        days += self.get_boxing_day(year)

        return days


class Quebec(Canada, VictoriaDayMixin, StJeanBaptisteMixin, ThanksgivingMixin):
    "Quebec"
    include_easter_monday = True

    def get_variable_days(self, year):
        days = super(Quebec, self).get_variable_days(year)
        days += [
            (self.get_victoria_day(year)),
            (self.get_thanksgiving(year)),
        ]
        days += self.get_st_jean(year)

        return days


class BritishColumbia(Canada, VictoriaDayMixin, AugustCivicHolidayMixin,
                      ThanksgivingMixin, EarlyFamilyDayMixin):
    "British Columbia"

    include_good_friday = True

    FIXED_HOLIDAYS = Canada.FIXED_HOLIDAYS + (
        (11, 11, "Remembrance Day"),
    )

    def get_variable_days(self, year):
        days = super(BritishColumbia, self).get_variable_days(year)
        days += [
            (self.get_family_day(year)),
            (self.get_victoria_day(year)),
            (self.get_civic_holiday(year, "British Columbia Day")),
            (self.get_thanksgiving(year)),
        ]

        return days


class Alberta(Canada, LateFamilyDayMixin, VictoriaDayMixin, ThanksgivingMixin):
    "Alberta"
    include_good_friday = True

    FIXED_HOLIDAYS = Canada.FIXED_HOLIDAYS + (
        (11, 11, "Remembrance Day"),
    )

    def get_variable_days(self, year):
        days = super(Alberta, self).get_variable_days(year)
        days += [
            (self.get_family_day(year)),
            (self.get_victoria_day(year)),
            (self.get_thanksgiving(year)),
        ]

        return days


class Saskatchewan(Canada, LateFamilyDayMixin, VictoriaDayMixin,
                   RemembranceDayShiftMixin, AugustCivicHolidayMixin,
                   ThanksgivingMixin):
    "Saskatchewan"
    include_good_friday = True

    def get_variable_days(self, year):
        days = super(Saskatchewan, self).get_variable_days(year)
        days += [
            (self.get_family_day(year)),
            (self.get_victoria_day(year)),
            (self.get_civic_holiday(year)),
            (self.get_thanksgiving(year)),
        ]
        days += self.get_remembrance_day(year)

        return days


class Manitoba(Canada, LateFamilyDayMixin, VictoriaDayMixin,
               AugustCivicHolidayMixin, ThanksgivingMixin):
    "Manitoba"
    include_good_friday = True

    def get_variable_days(self, year):
        days = super(Manitoba, self).get_variable_days(year)
        days += [
            (self.get_family_day(year, "Louis Riel Day")),
            (self.get_victoria_day(year)),
            (self.get_civic_holiday(year)),
            (self.get_thanksgiving(year)),
        ]

        return days


class NewBrunswick(Canada, AugustCivicHolidayMixin):
    "New Brunswick"

    FIXED_HOLIDAYS = Canada.FIXED_HOLIDAYS + (
        (11, 11, "Remembrance Day"),
    )

    include_good_friday = True

    def get_variable_days(self, year):
        days = super(NewBrunswick, self).get_variable_days(year)
        days += [
            (self.get_civic_holiday(year)),
        ]
        return days


class NovaScotia(Canada, RemembranceDayShiftMixin, LateFamilyDayMixin):
    "Nova Scotia"

    include_good_friday = True

    def get_variable_days(self, year):
        days = super(NovaScotia, self).get_variable_days(year)
        days += (self.get_remembrance_day(year))

        if year >= 2015:
            days += [
                (self.get_family_day(year, "Viola Desmond Day")),
            ]

        return days


class PrinceEdwardIsland(Canada, LateFamilyDayMixin, RemembranceDayShiftMixin):
    "Prince Edward Island"

    include_good_friday = True

    def get_variable_days(self, year):
        days = super(PrinceEdwardIsland, self).get_variable_days(year)
        days += [
            (self.get_family_day(year, "Islander Day")),
        ]
        days += (self.get_remembrance_day(year))

        return days


class Newfoundland(Canada):
    "Newfoundland"
    include_good_friday = True


class Yukon(Canada, VictoriaDayMixin, ThanksgivingMixin):
    "Yukon"

    FIXED_HOLIDAYS = Canada.FIXED_HOLIDAYS + (
        (11, 11, "Remembrance Day"),
    )

    include_good_friday = True

    def get_variable_days(self, year):
        days = super(Yukon, self).get_variable_days(year)
        days += [
            (self.get_nth_weekday_in_month(year, 8, MON, 3),
             "Discovery Day"),
            (self.get_victoria_day(year)),
            (self.get_thanksgiving(year)),
        ]

        return days


class NorthwestTerritories(Canada, RemembranceDayShiftMixin, VictoriaDayMixin,
                           ThanksgivingMixin):
    "Northwest Territories"

    FIXED_HOLIDAYS = Canada.FIXED_HOLIDAYS + (
        (6, 21, "National Aboriginal Day"),
    )

    include_good_friday = True

    def get_variable_days(self, year):
        days = super(NorthwestTerritories, self).get_variable_days(year)
        days += [
            (self.get_victoria_day(year)),
            (self.get_thanksgiving(year)),
        ]

        days += (self.get_remembrance_day(year))

        return days


class Nunavut(Canada, VictoriaDayMixin, ThanksgivingMixin,
              RemembranceDayShiftMixin):
    "Nunavut"
    include_good_friday = True

    def get_variable_days(self, year):
        days = super(Nunavut, self).get_variable_days(year)
        days += [
            (self.get_victoria_day(year)),
            (self.get_thanksgiving(year)),
        ]

        days += (self.get_remembrance_day(year))
        nuvanutday = date(year, 7, 9)
        days += [(nuvanutday, "Nuvanut Day")]
        if nuvanutday.weekday() == SUN:
            days += [(date(year, 7, 10), "Nuvanut Day (Shift)")]

        return days
