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


def create_uuid_from_string(title):
    assert isinstance(title, str)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, title))


def load_metadata(blog_name):
    metadata_path = Path("data/data_lake") / blog_name / "metadata.xml"
    with open(metadata_path) as f:
        xml_text = f.read()

    parsed_xml = BeautifulSoup(xml_text, "xml")
    return parsed_xml


# ________________________________________________-

# TODO: Write a function that extracts links from XML file, ->
# TODO: -> Write function that extracts blog_text and other metadata like published, date etc with input of a link

# def GetLinks(item) -> str:
#     """Extract links from XML file stored locally"""
#     links = []
#     link_elements = item.find_all('link')
#     for link_element in link_elements:
#         link = link_element.text
#         links.append(link)
#     return links


def get_blog_text_mit(item) -> str:
    """extract blog text from mit source, returns str containing blog text"""
    raw_text = item.find("content:encoded").text
    soup = BeautifulSoup(raw_text, "html.parser")
    blog_text = soup.get_text()

    return blog_text


def get_blog_text_sd(item) -> str:
    """send request to sd site to get article contents and extract its text, returns str containing article text"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
    }
    url = item.find("link").text  # get url to article from xml
    response = requests.get(url, headers=headers)
    raw_text = response.text
    soup = BeautifulSoup(raw_text, "html.parser")
    blog_text = soup.find("div", id="text").get_text()  # article text is under div with id "text"

    return blog_text


def extract_articles_from_xml(parsed_xml, blog_name):
    articles = []
    for item in parsed_xml.find_all("item"):
        title = item.title.text
        unique_id = create_uuid_from_string(title)

        if is_cached(
            unique_id, "articles"
        ):  # if unique ID is found in the articles directory (already extracted)
            continue

        if blog_name == "mit":
            blog_text = get_blog_text_mit(item)

        if blog_name == "sd":
            blog_text = get_blog_text_sd(item)
            time.sleep(
                0.2
            )  # NOTE: sd requires sending a request to their site to get text so a delay between requests is used

        # if blog_name == "openai":
        #     blog_text = GetLinks(item)

        article_info = BlogInfo(
            unique_id=unique_id,
            title=title,
            description=item.description.text,
            link=item.link.text,
            blog_text=blog_text,
            published=pd.to_datetime(
                item.pubDate.text.replace("EDT", "-0400")
            ).date(),  # tzinfo does not know how to handle "EDT", replacing it with equivalent "-0400" (4 hours behind UTC)
            timestamp=datetime.now(),
        )

        articles.append(article_info)

    return articles


def save_articles(articles, blog_name):
    save_dir = Path(
        "data/data_warehouse", "articles", blog_name
    )  # NOTE: changed to articles / blog_name
    save_dir.mkdir(exist_ok=True, parents=True)
    for article in articles:
        save_path = save_dir / article.get_filename()
        with open(save_path, "w") as f:
            f.write(article.json(indent=2))


def main(blog_name):
    print(f"Processing {blog_name}")
    parsed_xml = load_metadata(blog_name)
    articles = extract_articles_from_xml(parsed_xml, blog_name)
    save_articles(articles, blog_name)
    print(f"Done processing {blog_name}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blog_name", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    # get_blog_text_openai()
    args = parse_args()
    main(blog_name=args.blog_name)


# import requests
# from bs4 import BeautifulSoup

# def extract_metadata_from_link(main_link, link_to_follow):
#     try:
#         # Step 1: Send an HTTP GET request to the main link
#         main_response = requests.get(main_link)
#         main_response.raise_for_status()

#         # Parse the HTML content of the main page
#         main_soup = BeautifulSoup(main_response.text, 'html.parser')

#         # Step 2: Extract the link to follow
#         follow_link = main_soup.find('a', href=link_to_follow)

#         if follow_link:
#             # Construct the absolute URL for the link to follow
#             absolute_follow_link = main_link + follow_link['href']

#             # Send an HTTP GET request to the link to follow
#             follow_response = requests.get(absolute_follow_link)
#             follow_response.raise_for_status()

#             # Parse the HTML content of the linked page
#             follow_soup = BeautifulSoup(follow_response.text, 'html.parser')

#             # Extract information from the linked page
#             metadata = {}

#             # Extract blog text
#             blog_text = ''
#             for paragraph in follow_soup.find_all('p'):
#                 blog_text += paragraph.text + '\n'

#             metadata['blog_text'] = blog_text.strip()

#             # Extract other metadata (add more fields as needed)
#             # metadata['published_date'] = follow_soup.find('span', class_='published-date').text

#             return metadata

#         else:
#             print("Link to follow not found on the main page.")
#             return None

#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
#         return None

# # Example usage:
# if __name__ == "__main__":
#     main_link = "https://example.com/"
#     link_to_follow = "/sample-blog-link"
#     metadata = extract_metadata_from_link(main_link, link_to_follow)
#     if metadata:
#         print("Blog Text:")
#         print(metadata['blog_text'])
