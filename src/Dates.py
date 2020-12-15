class Dates:
    def __init__(self):
        self._date_set = set()

    @staticmethod
    def of(timePeriod):
        result = Dates()
        if isinstance(timePeriod, Year):
            for i in range(1, CalendarMonth.NUM_MONTHS+1):
                result._date_set.add(CalendarMonth(i, timePeriod.get_year()))

        elif isinstance(timePeriod, CalendarMonth):
            result._date_set.add(timePeriod)

        else:
            raise TypeError("Time period must be either a CalendarMonth or a Year")

        return result

    @staticmethod
    def range(beginPeriod, endPeriod):
        if not (isinstance(beginPeriod, Year) or isinstance(beginPeriod, CalendarMonth)) or not (isinstance(endPeriod, Year) or isinstance(endPeriod, CalendarMonth)):
            raise TypeError("Time periods must be either CalendarMonths or Years")
        if (isinstance(beginPeriod, CalendarMonth) and not isinstance(endPeriod, CalendarMonth)) or (isinstance(beginPeriod, Year) and not isinstance(endPeriod, Year)):
            raise TypeError("Begin period and end period type must match (either both CalendarMonth or both Year)")

        if beginPeriod.is_after(endPeriod):
            raise ValueError("Begin period must be before or equal to end period; Begin: "+str(beginPeriod)+" End: "+str(endPeriod))

        result = Dates()
        if(isinstance(beginPeriod, Year)):
            for year in range(beginPeriod.get_year(), endPeriod.get_year()+1):
                for month in range(1, CalendarMonth.NUM_MONTHS+1):
                    result._date_set.add(CalendarMonth(month, year))
        else:
            curr_year = beginPeriod.get_year()
            curr_month = beginPeriod.get_month()
            end_year = endPeriod.get_year()
            end_month = endPeriod.get_month()
            while(not (curr_month == end_month and curr_year == end_year)):
                result._date_set.add(CalendarMonth(curr_month, curr_year))
                curr_month+=1
                if(curr_month > CalendarMonth.NUM_MONTHS):
                    curr_month = 1
                    curr_year+=1
            result._date_set.add(CalendarMonth(end_month, end_year))
        return result

    def get_months(self):
        return list(self._date_set)

    @staticmethod
    def union(dates1, dates2):
        if not isinstance(dates1, Dates) or not isinstance(dates2, Dates):
            raise TypeError("Both objects must be and instance of Dates")

        result = Dates()
        result._date_set = dates1._date_set.union(dates2._date_set)
        return result

    def __repr__(self):
        return str(self.get_months())


class Year:
    def __init__(self, year):
        if not isinstance(year, int):
            raise TypeError("Year must be constructed using an integer to represent a valid year")
        
        self._year = year

    def get_year(self):
        return self._year

    def is_before(self, other):
        if isinstance(other, Year) or isinstance(other, CalendarMonth):
            return self._year < other.get_year()
        else:
            raise TypeError("Other must be a Year or CalendarMonth")

    def is_after(self, other):
        if isinstance(other, Year) or isinstance(other, CalendarMonth):
            return self._year > other.get_year()
        else:
            raise TypeError("Other must be a Year or CalendarMonth")

    def __repr__(self):
        return str(self._year)

    def __eq__(self, other):
        if isinstance(other, Year):
            return self._year == other._year
        return False

    def __hash__(self):
        return hash(self._year)

class CalendarMonth:
    NUM_MONTHS = 12
    def __init__(self, month, year):
        if not isinstance(month, int) or not isinstance(year, int):
            raise TypeError("CalendarMonth must be constructed using an integer representation for both the month and year. For example, July 1998 would be constructed as CalendarMonth(7, 1998): "+str(month)+", "+str(year))

        if month <= 0 or month > CalendarMonth.NUM_MONTHS:
            raise ValueError("Month parameter must be between 1 and 12 (inclusive): "+str(month))
        
        self._month = month
        self._year = year

    def get_month(self):
        return self._month

    def get_year(self):
        return self._year

    def is_before(self, other):
        if isinstance(other, Year):
            return self._year < other.get_year()
        elif isinstance(other, CalendarMonth):
            if self._year < other._year:
                return True
            elif self._year == other._year:
                return self._month < other._month
            else:
                return False
        else:
            raise TypeError("Other must be a Year or CalendarMonth")

    def is_after(self, other):
        if isinstance(other, Year):
            return self._year > other.get_year()
        elif isinstance(other, CalendarMonth):
            if self._year > other._year:
                return True
            elif self._year == other._year:
                return self._month > other._month
            else:
                return False
        else:
            raise TypeError("Other must be a Year or CalendarMonth")

    def __eq__(self, other):
        if isinstance(other, CalendarMonth):
            return self._month == other._month and self._year == other._year
        return False

    def __repr__(self):
        return f"{self.get_year()}/{self.get_month():02d}"

    def __lt__(self, other):
        if not isinstance(other, CalendarMonth):
            raise TypeError("Can only compare with other CalendarMonth objects")

        return self.is_before(other)

    def __hash__(self):
        return hash((self._month, self._year))
