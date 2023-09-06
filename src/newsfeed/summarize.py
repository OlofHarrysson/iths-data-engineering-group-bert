import argparse
import json
import os
import re

import openai
from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from textsum.summarize import Summarizer

from newsfeed.datatypes import BlogInfo
from newsfeed.get_cached_files import data_directory_path, is_cached

# Load dotenv in order to use the OpenAi API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_text(blog_text, summary_type):
    # Create a document object list for the library
    messages = [
        {
            "role": "system",
            "content": (
                "You are going to summarize the following blog in a short and concise manner, max 100 words, ideally less:"
                if summary_type == "tech"
                else "You are going to summarize the following blog for a non-technical person in a short and concise manner, max 100 words, ideally less:"
            ),
        },
        {"role": "user", "content": blog_text},
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0)
    return response.choices[0].message.content


def summarize_local_model(blog_text):
    summarizer = Summarizer()
    summarized_text = summarizer.summarize_string(blog_text)
    print(summarized_text)
    return summarized_text


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

    # NOTE: code not tested properly
    for dir in os.listdir(os.path.join(data_directory_path, "articles")):
        article_directories.append(dir)

    return article_directories


def summarize_articles(summary_type, model_type):
    """summarize all articles into summary_type, i.e. tech or nontech, if they are not already summarized"""

    article_directories = get_article_directories()
    summary_dir = f"{summary_type}_summaries"  # i.e. tech_summaries or nontech_summaries etc

    for dir in article_directories:
        os.makedirs(
            os.path.dirname(data_directory_path + f"/{summary_dir}/" + dir + "/"),
            exist_ok=True,
        )

        blogs = read_articles(data_directory_path + "articles/" + dir)

        for blog in blogs:
            # Check if the blog summary already exists
            if not is_cached(
                blog.unique_id, summary_dir
            ):  # goes into data warehouse / summary_dir and searches for matching ID
                # Remove file name characters disallowed by the filesystem
                file_name = BlogInfo.get_filename(blog)

                print(f"summarizing: {file_name[:10]}...")

                if model_type == "api":
                    summary = summarize_text(blog.blog_text, summary_type)
                else:
                    summary = summarize_local_model(blog.blog_text)

                # Follow BlogSummary schema
                blog_summary = {
                    "unique_id": blog.unique_id,
                    "title": blog.title,
                    "summary": summary,
                    "link": blog.link,
                    "published": str(blog.published),
                }

                with open(
                    data_directory_path
                    + f"/{summary_type}_summaries/"
                    + dir
                    + "/"
                    + file_name
                    + ".json",
                    "w",
                ) as file:
                    json.dump(blog_summary, file, indent=4)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--summary_type",
        type=str,
        default="tech",
        choices=["tech", "nontech"],
        help='Choose either "tech" or "nontech" as the type of summary',
    )
    parser.add_argument("--model_type", type=str, default="api", choices=["api", "local_model"])
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    summarize_articles(summary_type=args.summary_type, model_type=args.model_type)
