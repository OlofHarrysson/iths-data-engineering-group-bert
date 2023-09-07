import os

# count amount of files in folder data_warehouse
file_count = sum(len(files) for _, _, files in os.walk(r"data/data_warehouse/articles"))
print(file_count)


def compare_articles():
    pass
