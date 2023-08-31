from textsum.summarize import Summarizer

from newsfeed.summarize import summarize_local_model


def test_local_model_inference():
    text = """This is a test"""
    summary = summarize_local_model(text)
    print(f"Summary: {summary}")
