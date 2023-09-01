import json
import os

from newsfeed.datatypes import BlogSummary

data_directory_path = "data/data_warehouse/"


def get_file_paths(filetype):  # NOTE: filetype is "article", "tech", or "nontech"
    all_files = []

    # loop through and get all files in the summaries folder
    for root, _, files in os.walk(data_directory_path + filetype):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    return all_files


def load_data_from_json_file(file_path):
    # Load the file data
    with open(file_path, "r") as file:
        json_data = json.load(file)
        # TODO if summary:
        data_model = BlogSummary(**json_data)
        # TODO if article:
        # create BlogInfo object
        return data_model


def get_contents(filetype):
    files = get_file_paths(filetype)
    contents = []

    for file_path in files:
        contents.append(load_data_from_json_file(file_path))

    return contents


# Check if the id of the file already exists. if so, it can be excluded
def check_cache(id, filetype):
    contents = get_contents(filetype)

    for content in contents:
        if content.unique_id == id:
            return True

    return False
