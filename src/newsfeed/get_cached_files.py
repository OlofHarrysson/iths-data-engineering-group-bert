import json
import os

from newsfeed.datatypes import BlogSummary

data_directory_path = "data/data_warehouse/"


def get_file_paths():  # TODO: add type of file "technical" "non-technical" "article"
    all_files = []

    # loop through and get all files in the summaries folder
    for root, _, files in os.walk(data_directory_path + "summaries"):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    return all_files


def load_data_from_json_file(file_path):
    # Load the summary data into a BlogSummary object
    with open(file_path, "r") as file:
        json_data = json.load(file)
        data_model = BlogSummary(**json_data)
        return data_model


def get_contents():
    summary_files = get_file_paths()
    summaries = []

    for file_path in summary_files:
        summaries.append(load_data_from_json_file(file_path))

    return summaries


# Check if the id of the file already exists in the summaries. if so, a new summary isn't needed
def check_cache(id):
    summaries = get_contents()

    for summary in summaries:
        if summary.unique_id == id:
            return True

    return False
