import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from newsfeed.get_cached_files import data_directory_path


def save_timestamp():
    with open("data/data_warehouse/timestamps.txt", "w") as file:
        time = datetime.now()
        file.write(str(time) + "\n")


def get_timestamp():
    timestamp_path = Path(data_directory_path + "pipeline_ran.txt")
    with open(timestamp_path, "r") as file:
        text = file.read()

        # parse date and time from the text
        datetime_obj = datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f")

        # format date as "yyyy-mm-dd"
        formatted_timestamp = datetime_obj.strftime("%Y-%m-%d")

    return formatted_timestamp


if __name__ == "__main__":
    # save timestamp to data warehouse (used to see when pipeline was last ran)
    save_timestamp()
