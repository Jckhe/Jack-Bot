from datetime import datetime, timedelta
from dateutil import tz

def get_weekday_or_previous_friday(current_timezone_str):
    # Get the current timezone
    current_timezone = tz.gettz(current_timezone_str)

    # Get the current time in the specified timezone
    current_time = datetime.now(current_timezone)
    # Calculate the date to return based on the day of the week
    if current_time.weekday() == 5:  # Saturday
        previous_friday = current_time - timedelta(days=1)
        return previous_friday.strftime('%Y-%m-%d')
    elif current_time.weekday() == 6: 
        previous_friday = current_time - timedelta(days=2)
        return previous_friday.strftime('%Y-%m-%d')
    else:
        return current_time.strftime('%Y-%m-%d')  # Return the current date in 'YYYY-MM-DD' format
