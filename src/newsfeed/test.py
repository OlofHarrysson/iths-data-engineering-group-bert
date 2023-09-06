import argparse
import time
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

from newsfeed.datatypes import BlogInfo
from newsfeed.get_cached_files import is_cached

# TODO: How can i find the xml_path automatically without hardcoding it?
xml_path = "data/data_lake/openai/metadata.xml"


def getLinks(xml_path):
    links = []

    # read the contents of the xml file
    with open(xml_path, "r") as file:
        xml_content = file.read()
    # parse xml content
    soup = BeautifulSoup(xml_content, "xml")
    # find all the <links> within tag <item>
    link_elements = soup.find_all("link")

    for link_element in link_elements:
        link = link_element.text
        links.append(link)

    return links


# links = getLinks(xml_path)
# print(links)

# ____ORIGINAL CODE_____

# def get_blog_text_openai(link) -> str:
#     """Extract blog text from function getLinks and return str containing blog text"""
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
#     }
#     response = requests.get(link, headers=headers)
#     raw_text = response.text
#     soup = BeautifulSoup(raw_text, "html.parser")
#     content = soup.find(id="content").text
#     print(content)
#     asdas
#     return link
# _________________________________________-


def get_blog_text_openai(link) -> str:
    """Extract blog text from function getLinks and return str containing blog text"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
    }
    response = requests.get(link, headers=headers)
    raw_text = response.text
    soup = BeautifulSoup(raw_text, "html.parser")
    content = soup.find(id="content").get_text()
    print(content)
    asd
    return link


link = "https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates"
output = get_blog_text_openai(link)
print(output)


# blog_text = soup.find("div", id="text").get_text()


# def get_blog_text_mit(item) -> str:
#     """extract blog text from mit source, returns str containing blog text"""
#     raw_text = item.find("content:encoded").text
#     soup = BeautifulSoup(raw_text, "html.parser")
#     blog_text = soup.get_text()


#     return blog_text
