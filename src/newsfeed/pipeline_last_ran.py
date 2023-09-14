import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from newsfeed.get_cached_files import data_directory_path


def save_timestamp():
    with open(data_directory_path + "pipeline_ran.txt", "w") as file:
        time = datetime.now()
        file.write(str(time))


def get_timestamp():
    timestamp_path = Path(data_directory_path + "pipeline_ran.txt")
    with open(timestamp_path, "r") as file:
        text = file.read()

    timestamp = datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f")
    return timestamp


def time_since_pipeline_ran():
    # datetime_str = "2023-09-14 09:47:48.079068"
    timestamp = get_timestamp()

    # Get the current datetime
    current_datetime = datetime.now()

    # Calculate the time difference
    time_difference = current_datetime - timestamp

    # Extract the number of days, seconds, and microseconds from the time difference
    days = time_difference.days
    seconds = time_difference.seconds
    microseconds = time_difference.microseconds

    # Calculate the total number of seconds
    total_seconds = days * 24 * 3600 + seconds + microseconds / 1e6

    # Define thresholds for different units of time
    minute_threshold = 60
    hour_threshold = 60 * minute_threshold
    day_threshold = 24 * hour_threshold

    # Format the time difference
    if total_seconds < minute_threshold:
        result = f"{int(total_seconds)} seconds ago"
    elif total_seconds < hour_threshold:
        result = f"{int(total_seconds / minute_threshold)} minutes ago"
    elif total_seconds < day_threshold:
        result = f"{int(total_seconds / hour_threshold)} hours ago"
    else:
        result = f"{int(total_seconds / day_threshold)} days ago"

    return result


if __name__ == "__main__":
    # save timestamp to data warehouse (used to see when pipeline was last ran)
    save_timestamp()
    print(f"Pipeline ran at {datetime.now()} (timestamp saved)")
