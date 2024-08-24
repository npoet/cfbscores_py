from datetime import datetime
import pytz


def convert_time(timestring):
    """
    convert_time outputs readable game times from ESPN timestamps (formerly shortDetail, see commit history for fun)
    :param timestring: ESPN UTC timestamp
    :return: replacement string converted to local time, i.e. "10/14 - 8:00 PM"
    """
    utc_dt = datetime.strptime(timestring, "%Y-%m-%dT%H:%MZ")
    utc_zone = pytz.utc

    # Define the Pacific Daylight Time timezone
    pdt_zone = pytz.timezone("America/Los_Angeles")

    # Convert UTC time to PDT
    utc_dt = utc_zone.localize(utc_dt)
    pdt_dt = utc_dt.astimezone(pdt_zone)

    month_day = f"{pdt_dt.month}/{pdt_dt.day}"
    hour_minute = pdt_dt.strftime("%I:%M %p").lstrip("0")  # Strip leading zero from hour

    formatted_time = f"{month_day} - {hour_minute}"

    return formatted_time
