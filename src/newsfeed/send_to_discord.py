import requests

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

    # try:
    #     result = requests.post(webhook_url, json=data)
    #     result.raise_for_status()  # Check for HTTP errors
    # except requests.exceptions.RequestException as req_err:
    #     print(
    #         "An error occurred during the request:", req_err
    #     )  # Handle connection errors, timeouts, and other request-related issues here
    # except requests.exceptions.HTTPError as http_err:
    #     print("HTTP error:", http_err)
    #     print("Response text:", result.text)
    #     # Handle HTTP errors, such as 4xx and 5xx status codes, here
    # except Exception as err:
    #     print("An unexpected error occurred:", err)  # Handle any other errors here
    # else:
    #     print(
    #         "Payload delivered successfully, code {}.".format(result.status_code)
    #     )  # If no errors occurred, print the result code


if __name__ == "__main__":
    summaries = get_contents(
        "tech_summaries"
    )  # when ran, sends all tech_summaries to our summary text chat

    for summary in summaries:
        send_summary(
            title=summary.title,
            content=summary.summary,
            published=str(summary.published),
            article_url=summary.link,
        )
