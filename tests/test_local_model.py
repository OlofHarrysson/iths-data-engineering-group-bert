from textsum.summarize import Summarizer


def test_local_model_inference():
    text = """This is a test"""
    summarizer = Summarizer()
    summary = summarizer.summarize_string(text)
    print(f"Summary: {summary}")
