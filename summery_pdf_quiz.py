from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
import dotenv
import os

def read_pdf_and_summerize(path):
    dotenv.load_dotenv()
    api_key = ''
    os.environ['OPENAI_API_KEY'] = api_key
    loader = PyPDFLoader(path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)
    prompt_template = """Write a concise summary of the following extracting the key information:
    Text: `{text}`
    CONCISE SUMMARY:"""
    initial_prompt = PromptTemplate(template=prompt_template, input_variables=['text'])

    refine_template = '''
        Your job is to produce a final quiz.
        I have provided an existing summary up to a certain point: {existing_answer}.
        Please Write 3 question with 4 options and correct  answer based on the following text.
        TEXT: `{text}
        ------------
        

    '''
    refine_prompt = PromptTemplate(
        template=refine_template,
        input_variables=['existing_answer', 'text']
    )
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    chain = load_summarize_chain(
        llm=llm,
        chain_type='refine',
        question_prompt=initial_prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=False

    )
    output_summary = chain.run(chunks)
    return output_summary

