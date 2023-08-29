import argparse
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

from newsfeed.datatypes import BlogInfo


def create_uuid_from_string(title):
    assert isinstance(title, str)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, title))


def load_metadata(blog_name):
    metadata_path = Path("data/data_lake") / blog_name / "metadata.xml"
    with open(metadata_path) as f:
        xml_text = f.read()

    parsed_xml = BeautifulSoup(xml_text, "xml")
    return parsed_xml


def extract_articles_from_xml(parsed_xml, blog_name):
    articles = []
    for item in parsed_xml.find_all("item"):
        if blog_name == "mit":
            raw_blog_text = item.find("content:encoded").text
            soup = BeautifulSoup(raw_blog_text, "html.parser")
            blog_text = soup.get_text()

        if blog_name == "sd":
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
            }
            url = item.find("link").text
            response = requests.get(url, headers=headers)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            textest = soup.find("div", id="text")
            blog_text = textest.get_text()
            break

        title = item.title.text
        unique_id = create_uuid_from_string(title)
        article_info = BlogInfo(
            unique_id=unique_id,
            title=title,
            description=item.description.text,
            link=item.link.text,
            blog_text=blog_text,
            published=pd.to_datetime(item.pubDate.text).date(),
            timestamp=datetime.now(),
        )
        articles.append(article_info)
        print(articles)

    return articles


def save_articles(articles, blog_name):
    save_dir = Path("data/data_warehouse", blog_name, "articles")
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
    args = parse_args()
    main(blog_name=args.blog_name)
