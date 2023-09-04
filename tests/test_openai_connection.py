import requests


def test_openai_connection():
    # test if summarization is possible
    requests.get("https://openai.com/", timeout=10)


if __name__ == "__main__":
    test_openai_connection()
