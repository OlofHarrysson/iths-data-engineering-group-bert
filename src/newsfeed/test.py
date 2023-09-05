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


links = getLinks(xml_path)
print(links)


# def get_blog_text_openai(links) -> str:
#     """Extract blog text from function getLinks and return str containing blog text"""
#     soup = BeautifulSoup(raw_text, "html.parser")
#     raw_text = links.find("div", class_="ui-blocks").text
#     links = soup.get_text()
#     return links


# output = get_blog_text_openai(links)
# print(output)

# def get_blog_text_mit(item) -> str:
#     """extract blog text from mit source, returns str containing blog text"""
#     raw_text = item.find("content:encoded").text
#     soup = BeautifulSoup(raw_text, "html.parser")
#     blog_text = soup.get_text()


#     return blog_text
