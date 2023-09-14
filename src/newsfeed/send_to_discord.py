import argparse

# from newsfeed.count_articles import extract_timestamps_from_json_files
from datetime import date, datetime, timedelta
from urllib.parse import urlparse

import requests

from newsfeed.filter_summarized_articles import (
    amount_summaries_from_each_source,
    sort_summaries,
)
from newsfeed.get_cached_files import get_contents


def send_summary(
    title="Article title",
    content="Article content",
    published="date",
    article_url="https://www.example.com",
):
    webhook_url = "https://discord.com/api/webhooks/1143844243111170199/n5PipEY2WvDVniMpsJC-wXnrUN2q7aG18HqsG7wpm_Qu3MjuyIulsR3LKC64hziTsHM3"  # URL of the webhook

    data = {"username": "BertSummary"}  # Name shown in discord when message is sent

    data["embeds"] = [  # The message that is sent
        {
            "color": 0xEDCE7,  # Color of the message
            "title": title,  # Title of the article, REPLACE WITH ACTUAL TITLE!!
            "fields": [  # Fields are the different sections of the message
                {
                    "name": "Summary:",  # Name of the field
                    "value": content,  # The summarized content of the article, REPLACE WITH ACTUAL CONTENT!!
                    "inline": False,  # If true the field will be side by side with the previous field, keep false please
                },
                {
                    "name": "Published:",  # Name of the field
                    "value": published,  # The summarized content of the article, REPLACE WITH ACTUAL CONTENT!!
                    "inline": False,  # If true the field will be side by side with the previous field, keep false please
                },
            ],
            "footer": {"text": "Group: Bert"},
            "url": article_url,  # URL of the article, REPLACE WITH ACTUAL URL!!,
        },
    ]

    result = requests.post(webhook_url, json=data)
    result.raise_for_status()  # Check for HTTP errors


def main(summary_type):
    summaries = get_contents(summary_type)

    summaries = sort_summaries(summaries)  # sort by date of each summary object
    summaries = summaries[::-1]  # reverse to get latest summary at the bottom in discord

    for summary in summaries:
        published_timestamp = summary.published

        # Calculate a timestamp 24 hours ago
        one_day_ago = datetime.now().date() - timedelta(hours=24)

        # Check if the published timestamp is within the last 24 hours and exists in the set
        if one_day_ago <= published_timestamp:
            print(f"Sending summary: {summary.title}")
            send_summary(
                title=summary.title,
                content=summary.summary,
                published=str(summary.published),
                article_url=summary.link,
            )
        else:
            print(f"Skipping summary: {summary.title}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--summary_type",
        type=str,
        default="tech_summaries",
        choices=[
            "tech_summaries",
            "nontech_summaries",
            "sv_nontech_summaries",
            "sv_tech_summaries",
        ],
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(summary_type=args.summary_type)
