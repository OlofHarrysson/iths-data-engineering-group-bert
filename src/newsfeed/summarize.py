import json
import os
import re

from datatypes import BlogInfo
from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document

# Load dotenv in order to use the OpenAi API key
load_dotenv()


def summarize_text(blog_text):
    # Create a document object list for the library
    docs = [Document(page_content=blog_text)]

    # declare the model with a temperature of 0 in order to maximize conciseness
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.run(docs)


directory_path = "data/data_warehouse/"


def read_articles_in_dir(dir):
    BlogInfo_list = []

    for filename in os.listdir(dir):
        if filename.endswith(".json"):
            file_path = os.path.join(dir, filename)

            BlogInfo_list.append(BlogInfo.parse_file(file_path))

    return BlogInfo_list


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
        BlogInfo_list = read_articles_in_dir(directory_path + dir + "/articles")

        for BlogInfo in BlogInfo_list:
            file_name = re.sub(r'[\/:*?"<>|]', "", BlogInfo.title.replace(" ", "_"))

            print(file_name)

            os.makedirs(
                os.path.dirname(directory_path + "/summaries/" + dir + "/articles/"), exist_ok=True
            )

            ff = summarize_text(BlogInfo.blog_text)

            j = {"unique_id": BlogInfo.unique_id, "title": BlogInfo.title, "text": ff}

            with open(
                directory_path
                + "/summaries/"
                + dir
                + "/articles/"
                + file_name
                + "SUMMARYSUMMARY.json",
                "w",
            ) as file:
                # file.write("content")
                json.dump(j, file, indent=4)


save_articles()
