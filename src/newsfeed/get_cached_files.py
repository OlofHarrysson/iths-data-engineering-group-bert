import json
import os

from newsfeed.datatypes import BlogInfo, BlogSummary

data_directory_path = "data/data_warehouse/"


def get_file_paths(warehouse_dir):
    all_files = []

    # loop through and get all files in the summaries folder
    for root, _, files in os.walk(data_directory_path + warehouse_dir):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    return all_files


def load_data_from_json_file(file_path):
    # Load the file data
    with open(file_path, "r") as file:
        json_data = json.load(file)

        # if loading an article use the article datatype
        if file_path.startswith("data/data_warehouse/articles/"):
            data_model = BlogInfo(**json_data)

        # else use the summary datatype
        else:
            data_model = BlogSummary(**json_data)

        return data_model


def get_contents(warehouse_dir):
    files = get_file_paths(warehouse_dir)
    contents = []

    for file_path in files:
        contents.append(load_data_from_json_file(file_path))

    return contents


# Check if the id of the file already exists. if so, it can be excluded
def is_cached(id, warehouse_dir):
    contents = get_contents(warehouse_dir)

    for content in contents:
        if content.unique_id == id:
            return True

    return False