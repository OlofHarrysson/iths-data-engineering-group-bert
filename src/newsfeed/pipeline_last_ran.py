import json
import os
from datetime import datetime, timedelta


def timestamp_now():
    with open("data/data_warehouse/timestamp/timestamps.txt", "w") as file:
        time = datetime.now()
        file.write(str(time) + "\n")


# Call the function to execute it
timestamp_now()
