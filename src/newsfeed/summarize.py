from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader

# Load dotenv in order to use the OpenAi API key
load_dotenv()


def summarize_text(blog_text):
    # Download the text
    loader = WebBaseLoader(blog_text)
    docs = loader.load()

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")

    summary = chain.run(docs)

    return summary


# Example
if __name__ == "__main__":
    summary = summarize_text("https://lilianweng.github.io/posts/2023-06-23-agent/")
    print(summary)
