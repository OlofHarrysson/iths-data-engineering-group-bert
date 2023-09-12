import json
import os
from datetime import date


def extract_timestamps_from_json_files(parent_folder):
    timestamps = []

    for root, _, files in os.walk(parent_folder):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)

                try:
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        published_timestamp = data.get("published")

                        if published_timestamp:
                            published_date = date.fromisoformat(published_timestamp)
                            timestamps.append(published_date)
                        else:
                            print(f"Warning: No 'published' field in {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

    return timestamps


# Write timestamps in a .txt file
def write_timestamps_to_file(timestamps):
    with open("data/data_warehouse/timestamp/timestamps.txt", "w") as file:
        for timestamp in timestamps:
            file.write(str(timestamp) + "\n")


if __name__ == "__main__":
    parent_folder = r"data/data_warehouse/articles/"  # Define the parent folder containing the subfolders with JSON files
    timestamps = extract_timestamps_from_json_files(parent_folder)
    write_timestamps_to_file(timestamps)
    # for timestamp in timestamps:
    # print(timestamp)


# # count amount of files in folder data_warehouse
# file_count = sum(len(files) for _, _, files in os.walk(r"data/data_warehouse/articles"))
# print(file_count)
# Will out put first total amount of files in folder with subfolder data_warehouse that is json files
# second will output total amount of files in folder with subfolder data_warehouse/articles
