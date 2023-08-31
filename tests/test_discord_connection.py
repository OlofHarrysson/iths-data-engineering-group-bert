import requests


def test_discord_connection():
    requests.get("https://discord.com/", timeout=10)


if __name__ == "__main__":
    test_discord_connection()
