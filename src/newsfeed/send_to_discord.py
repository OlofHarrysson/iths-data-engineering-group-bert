import requests


def send_summary(title="Article title", content="Article content", url="https://www.example.com"):
    url = "https://discord.com/api/webhooks/1143844243111170199/n5PipEY2WvDVniMpsJC-wXnrUN2q7aG18HqsG7wpm_Qu3MjuyIulsR3LKC64hziTsHM3"  # URL of the webhook

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
                }
            ],
            "footer": {"text": "Group: Bert"},
            "url": url,  # URL of the article, REPLACE WITH ACTUAL URL!!
        },
    ]

    result = requests.post(url, json=data)  # Sends/posts the message

    try:  # Checks if the message was sent successfully
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:  # If not, prints the error
        print(err)
    else:  # If so, prints delivered and the status code
        print("Payload delivered successfully, code {}.".format(result.status_code))


# Example usage:
send_summary("Article title", "Article content", "https://www.example.com")
