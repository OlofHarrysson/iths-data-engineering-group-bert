import json
import os

import requests
from datatypes import BlogSummary
from summarize import data_directory_path


def get_summary_file_paths():
    all_files = []

    # loop through and get all files in the summaries folder
    for root, _, files in os.walk(data_directory_path + "summaries"):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    return all_files


def load_data_from_json_file(file_path):
    # Load the summary data into a BlogSummary object
    with open(file_path, "r") as file:
        json_data = json.load(file)
        data_model = BlogSummary(**json_data)
        return data_model


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

    try:
        result = requests.post(webhook_url, json=data)
        result.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as req_err:
        print(
            "An error occurred during the request:", req_err
        )  # Handle connection errors, timeouts, and other request-related issues here
    except requests.exceptions.HTTPError as http_err:
        print("HTTP error:", http_err)
        print("Response text:", result.text)
        # Handle HTTP errors, such as 4xx and 5xx status codes, here
    except Exception as err:
        print("An unexpected error occurred:", err)  # Handle any other errors here
    else:
        print(
            "Payload delivered successfully, code {}.".format(result.status_code)
        )  # If no errors occurred, print the result code


if __name__ == "__main__":
    summary_files = get_summary_file_paths()

    for file_path in summary_files:
        summary = load_data_from_json_file(file_path)

        send_summary(
            title=summary.title,
            content=summary.summary,
            published=str(summary.published),
            article_url=summary.link,
        )
