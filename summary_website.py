from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI
import dotenv
import os
import pprint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_extraction_chain

    

def scrape_with_playwright(urls):
    dotenv.load_dotenv()
    api_key = ''
    os.environ['OPENAI_API_KEY'] = api_key
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    schema = {
        "properties": {
            "news_article_title": {"type": "string"},
            "news_article_summary": {"type": "string"},
        },
        "required": ["news_article_title", "news_article_summary"],
    }

    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["span"]
    )
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)
    extracted_content= create_extraction_chain(schema=schema, llm=llm).run(splits[0].page_content)
    print(splits[0])
    pprint.pprint(extracted_content)
    return extracted_content
