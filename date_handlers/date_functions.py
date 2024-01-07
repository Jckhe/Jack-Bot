from datetime import datetime, timedelta

def yesterdayTimeString():
    # Get current UTC time
    utc_now = datetime.utcnow()

    # Calculate the time difference for PST (UTC-8)
    utc_pst_diff = timedelta(hours=8)

    # Convert current UTC time to PST
    pst_now = utc_now - utc_pst_diff

    # Calculate the time 24 hours ago in PST
    pst_yesterday = pst_now - timedelta(days=1)

    # Format the time 24 hours ago in the specified format
    yesterday_time_str = pst_yesterday.strftime("%Y-%m-%dT%H:%M:%S.%f0Z")

    return yesterday_time_str