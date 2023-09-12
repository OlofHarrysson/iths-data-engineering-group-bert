import argparse
from pathlib import Path

import requests
from bs4 import BeautifulSoup

LINK_TO_XML_FILE = {
    "mit": "https://news.mit.edu/rss/topic/artificial-intelligence2",
    "sd": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
    "openai": "https://jamesg.blog/openai.xml",
}


def get_metadata_info(blog_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
    }

    assert (
        blog_name in LINK_TO_XML_FILE
    ), f"{blog_name=} not supported. Supported blogs: {list(LINK_TO_XML_FILE)}"
    blog_url = LINK_TO_XML_FILE[blog_name]
    response = requests.get(blog_url, headers=headers)
    response.encoding = "utf-8"  # Specify the correct encoding
    print(response.status_code)
    xml_text = response.text

    return xml_text


def save_metadata_info(xml_text, blog_name):
    path_xml_dir = Path("data/data_lake") / blog_name
    path_xml_dir.mkdir(exist_ok=True, parents=True)
    with open(path_xml_dir / "metadata.xml", "w", encoding="utf-8") as f:
        f.write(xml_text)


def main(blog_name):
    print(f"Processing {blog_name}")
    xml_text = get_metadata_info(blog_name)
    save_metadata_info(xml_text, blog_name)
    print(f"Done processing {blog_name}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blog_name", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(blog_name=args.blog_name)
