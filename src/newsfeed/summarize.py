import json
import os
import re

from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document

from newsfeed.datatypes import BlogInfo

# Load dotenv in order to use the OpenAi API key
load_dotenv()


def summarize_text(blog_text):
    # Create a document object list for the library
    docs = [Document(page_content=blog_text)]

    # declare the model with a temperature of 0 in order to maximize conciseness
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.run(docs)


# summary = summarize_text2("test")
# print(summary)


directory_path = "data/data_warehouse/"


def read_articles_in_dir(dir):
    article_jsons = []

    for filename in os.listdir(dir):
        if filename.endswith(".json"):
            file_path = os.path.join(dir, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
                article_jsons.append(json_data)

    return article_jsons


def save_articles():
    # For future kev to deal with.
    # Fix bug where it fucks up if the articles directory is empty

    subdirectories = [
        d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))
    ]

    try:
        subdirectories.remove("summaries")
    except:
        pass

    for dir in subdirectories:
        article_jsons = read_articles_in_dir(directory_path + dir + "/articles")

        for article in article_jsons:
            file_name = re.sub(r'[\/:*?"<>|]', "", article["title"].replace(" ", "_"))

            print(file_name)

            os.makedirs(
                os.path.dirname(directory_path + "/summaries/" + dir + "/articles/"), exist_ok=True
            )

            with open(
                directory_path
                + "/summaries/"
                + dir
                + "/articles/"
                + file_name
                + "SUMMARYSUMMARY.json",
                "w",
            ) as file:
                file.write("content")


save_articles()
