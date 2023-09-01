from newsfeed.summarize import summarize_text


def test_chatgpt():
    # test if summarization is possible
    summarize_text("respond with 'ok'")


if __name__ == "__main__":
    test_chatgpt()
