import argparse
import json
import os
import re
from pathlib import Path

import openai
from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from textsum.summarize import Summarizer

from newsfeed.datatypes import BlogInfo
from newsfeed.get_cached_files import data_directory_path, is_cached

# import unidecode


# Load dotenv in order to use the OpenAi API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_text(blog_text, summary_type):
    # Define prompts for different combinations of language and summary_type
    prompts = {
        "tech": "You are Data Scientist. Could you please provide a concise and comprehensive technical summary of the given text? The summary should capture the main points and key details of the text while conveying the authors intended meaning accurately. Please ensure that the summary is well-organized and easy to read(This is the most important rule), with clear headings and subheadings to guide the reader through each section. The length of the summary max 75 words or less if possible, without including unnecessary information or becoming overly long:",
        "nontech": "You are an Popular Non technical Science Journalist. Could you please provide a concise and summary of the given text? The summary should capture the main points and key details of the text while conveying the authors intended meaning accurately. Please ensure that the summary is well-organized and easy to read(This is the most important rule), with clear headings and subheadings to guide the reader through each section. The length of the summary max 75 words or less if possible, without including unnecessary information or becoming overly long:",
        "sv_tech": "You are Data Scientist. Could you please provide a concise and comprehensive technical summary of the given text ONLY IN SWEDISH? The summary should capture the main points and key details of the text while conveying the authors intended meaning accurately. Please ensure that the summary is well-organized and easy to read(This is the most important rule), with clear headings and subheadings to guide the reader through each section. The length of the summary max 75 words or less if possible, without including unnecessary information or becoming overly long:",
        "sv_nontech": "You are an Popular Non technical Science Journalist. Could you please provide a concise and summary of the given text ONLY IN SWEDISH? The summary should capture the main points and key details of the text while conveying the authors intended meaning accurately. Please ensure that the summary is well-organized and easy to read(This is the most important rule), with clear headings and subheadings to guide the reader through each section. The length of the summary max 75 words or less if possible, without including unnecessary information or becoming overly long:",
    }

    prompt = prompts[(summary_type)]

    messages = [
        {
            "role": "system",
            "content": prompt,
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

    # Find all json files in the the directory and parse them
    files = Path(dir).glob("*.json")
    for file in files:
        # Use the BlogInfo object
        blog = BlogInfo.parse_file(file)
        blogs.append(blog)

    return blogs


def get_article_directories():
    article_directories = []

    # NOTE: code not tested properly
    for dir in os.listdir(os.path.join(data_directory_path, "articles")):
        article_directories.append(dir)

    return article_directories


def summarize_articles(summary_type, model_type):
    """summarize all articles into summary_type, i.e., tech or nontech, if they are not already summarized"""

    article_directories = get_article_directories()
    summary_dir = f"{summary_type}_summaries"  # i.e., tech_summaries or nontech_summaries, etc.

    for dir in article_directories:
        os.makedirs(
            os.path.dirname(data_directory_path + f"/{summary_dir}/" + dir + "/"),
            exist_ok=True,
        )

        blogs = read_articles(data_directory_path + "articles/" + dir)

        for blog in blogs:
            file_name = BlogInfo.get_filename(blog)
            # Check if the blog summary already exists
            if not is_cached(
                blog.unique_id, summary_dir
            ):  # goes into data warehouse / summary_dir and searches for matching ID
                # Remove file name characters disallowed by the filesystem

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
            else:
                print(f"skipped (cached): {file_name[:10]}...")


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--summary_type",
        type=str,
        default="tech",
        choices=["tech", "nontech", "sv_tech", "sv_nontech"],
        help='Choose either "tech" or "nontech" as the type of summary, there is also "sv_tech" and "sv_nontech" for swedish summaries',
    )
    parser.add_argument("--model_type", type=str, default="api", choices=["api", "local_model"])
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    summarize_articles(summary_type=args.summary_type, model_type=args.model_type)
