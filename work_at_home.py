import pandas as pd
import holidays

def count_working_days(year, month):
    # Define Swedish holidays
    swedish_holidays = holidays.Sweden(year)

    # Generate date range for the given month
    start_date = pd.Timestamp(year, month, 1)
    end_date = pd.Timestamp(year, month, pd.Period(year=year, month=month, freq='M').days_in_month)

    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    # Filter out weekends and holidays
    working_days = [date for date in date_range if date.weekday() < 5 and date not in swedish_holidays]

    return len(working_days)

# Example usage
year = 2025
month = 8  # May
at_office = 3/5
print(f"Working days in {month}/{year}: {count_working_days(year, month)}")

days = count_working_days(year, month)

print(f'You should be {days*at_office} at office during the month')

print(f'or  {days - days*at_office} at home during the month')