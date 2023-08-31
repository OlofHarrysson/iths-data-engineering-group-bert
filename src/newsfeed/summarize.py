import argparse
import json
import os
import re

from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from textsum.summarize import Summarizer

from newsfeed.datatypes import BlogInfo
from newsfeed.get_summaries import check_summary_cache, data_directory_path

# Load dotenv in order to use the OpenAi API key
load_dotenv()


def summarize_text(blog_text):
    # Create a document object list for the library
    docs = [Document(page_content=blog_text)]

    # declare the model with a temperature of 0 in order to maximize conciseness
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.run(docs)


def summarize_local_model(blog_text):
    # docs = [Document(page_content=blog_text)]

    summarizer = Summarizer()
    summarized_text = summarizer.summarize_string(blog_text)
    print(summarized_text)
    return summarized_text
    # I'm not sure it shall return summarized_text
    # return summarized_text(docs)


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
        article_directories.remove("summaries/articles")
    except:
        pass

    return article_directories


def summarize_articles(model_type):
    # For future kev to deal with.
    # Fix bug where it fucks up if the articles directory is empty

    article_directories = get_article_directories()

    for dir in article_directories:
        os.makedirs(os.path.dirname(data_directory_path + "/summaries/" + dir + "/"), exist_ok=True)

        blogs = read_articles(data_directory_path + dir)

        for blog in blogs:
            if check_summary_cache(blog.unique_id):
                print(f"Summary {blog.get_filename()} already exists.")
            else:
                # Remove file name characters disallowed by the filesystem
                file_name = re.sub(r'[\/:*?"<>|]', "", blog.title.replace(" ", "_"))

                print(f"summarizing: {file_name[:10]}...")

                if model_type == "api":
                    summary = summarize_text(blog.blog_text)
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
                    data_directory_path + "/summaries/" + dir + "/" + file_name + ".json",
                    "w",
                ) as file:
                    json.dump(blog_summary, file, indent=4)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", type=str, default="api", choices=["api", "local_model"])
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    summarize_articles(args.model_type)
