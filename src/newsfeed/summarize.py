from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document

# Load dotenv in order to use the OpenAi API key
load_dotenv()


def summarize_text(blog_text):
    # Create a document object list for the library
    docs = [Document(page_content=blog_text)]

    # declare the model with a temperature of 0 in order to maximize conciseness
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.run(docs)


summary = summarize_text("test")
print(summary)
