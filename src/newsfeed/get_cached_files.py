import json
import os

from newsfeed.datatypes import BlogInfo, BlogSummary

data_directory_path = "data/data_warehouse/"


def get_file_paths(warehouse_dir):
    all_files = []

    # loop through and get all files in the summaries folder
    for root, _, files in os.walk(data_directory_path + warehouse_dir):
        for file in files:
            all_files.append(os.path.join(root, file))

    return all_files


def load_blog_info(file_path):
    # Load the file data
    with open(file_path, "r") as file:
        json_data = json.load(file)
    data_model = BlogInfo(**json_data)
    return data_model


def load_blog_summary(file_path):
    # Load the file data
    with open(file_path, "r") as file:
        json_data = json.load(file)
    data_model = BlogSummary(**json_data)
    return data_model


def get_contents(warehouse_dir):
    files = get_file_paths(warehouse_dir)

    # create a list of articles if dir is articles, else a list of summaries of the respective subdirectory (tech, nontech, etc)
    contents = [
        load_blog_info(file_path) if "/articles/" in file_path else load_blog_summary(file_path)
        for file_path in files
    ]

    return contents


# Check if the id of the file already exists. if so, it can be excluded
def is_cached(id, warehouse_dir):
    content_ids = set([content.unique_id for content in get_contents(warehouse_dir)])
    return id in content_ids


if __name__ == "__main__":
    # for manually checking for cached files, specify an id and run this script directly
    id = "e7a612ec-0088-5be9-ac17-eb7b75c3595e"
    content_ids = set([content.unique_id for content in get_contents("tech_summaries")])

    print(f"\n{len(content_ids)=}")
    print(f"{id in content_ids=}\n")
