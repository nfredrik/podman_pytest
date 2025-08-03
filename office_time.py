import calendar
from datetime import date
import holidays
from loguru import logger


def calculate_remote_days(year: int, month: int, office_percentage: float) -> float:
    """
    Beräknar antalet arbetsdagar du kan arbeta hemifrån under en given månad.

    Parametrar:
        year: Årtalet för beräkningen.
        month: Månaden (1-12).
        office_percentage: Procentsatsen du måste vara på kontoret (0-100).

    Returnerar:
        Totala antalet dagar att arbeta hemifrån.
    """
    # Hämta svenska helgdagar för det angivna året
    swedish_holidays = holidays.Sweden(years=year)

    # Räkna ut antalet faktiska arbetsdagar (måndag-fredag samt ej helgdag)
    working_days = 0
    _, last_day = calendar.monthrange(year, month)
    for day in range(1, last_day + 1):
        current_date = date(year, month, day)
        # weekday(): 0 = måndag ... 6 = söndag
        if current_date.weekday() < 5 and current_date not in swedish_holidays:
            working_days += 1

    # Antal hemmardagar = totala arbetsdagar * (100 - office_percentage) / 100
    remote_days = working_days * (100 - office_percentage) / 100
    return remote_days


# Exempelanvändning
if __name__ == "__main__":
    year = 2025
    month = 8
    office_percentage = 60  # Exempel: 60% av dagarna på kontoret = 40% hemma
    remote = calculate_remote_days(year, month, office_percentage)
    logger.info(f"Du kan arbeta hemifrån ca {remote:.2f} dagar under {month}/{year}.")
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
    logger.debug('debug')
    logger.info('info')
    logger.success('success')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
    logger.debug('debug')
    logger.info('info')
    logger.success('success')
