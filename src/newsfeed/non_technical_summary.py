import json
import os
import re

import openai
from datatypes import BlogInfo
from dotenv import load_dotenv
from get_summaries import check_summary_cache, data_directory_path

# Load dotenv in order to use the OpenAi API key
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def nontech_summarize_text(blog_text):
    messages = [
        {
            "role": "system",
            "content": "You are going to summarize the following blog for a non-technical person:",
        },
        {"role": "user", "content": blog_text},
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0)
    return response.choices[0].message.content


def read_articles(dir):
    blogs = []

    # Find all files in the the directory and parse them
    for filename in os.listdir(dir):
        if filename.endswith(".json"):
            file_path = os.path.join(dir, filename)

            # Use the BlogInfo object
            blog = BlogInfo.parse_file(file_path)
            blogs.append(blog)

    return blogs


def get_article_directories():
    article_directories = []

    # Make a list of all article directories
    for dir in os.listdir(data_directory_path):
        if os.path.isdir(os.path.join(data_directory_path, dir)):
            article_directories.append(dir + "/articles")

    # Remove summaries directory from list, as we don't wanna summarize the summaries
    try:
        article_directories.remove("nontech_summaries/articles")
        article_directories.remove("summaries/articles")

    except:
        pass

    return article_directories


def nontech_summarize_articles():
    # For future kev to deal with.
    # Fix bug where it fucks up if the articles directory is empty

    article_directories = get_article_directories()

    for dir in article_directories:
        os.makedirs(
            os.path.dirname(data_directory_path + "/nontech_summaries/" + dir + "/"), exist_ok=True
        )

        blogs = read_articles(data_directory_path + dir)

        for blog in blogs:
            # Check if the blog summary already exists
            if not check_summary_cache(blog.unique_id):
                # Remove file name characters disallowed by the filesystem
                file_name = re.sub(r'[\/:*?"<>|]', "", blog.title.replace(" ", "_"))

                print(f"summarizing ({dir}): {file_name[:10]}...")

                summary = nontech_summarize_text(blog.blog_text)

                # Follow BlogSummary schema
                blog_summary = {
                    "unique_id": blog.unique_id,
                    "title": blog.title,
                    "summary": summary,
                    "link": blog.link,
                    "published": str(blog.published),
                }

                with open(
                    data_directory_path + "/nontech_summaries/" + dir + "/" + file_name + ".json",
                    "w",
                ) as file:
                    json.dump(blog_summary, file, indent=4)


if __name__ == "__main__":
    nontech_summarize_articles()
