from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import MongoDBAtlasVectorSearch
from PyPDF2 import PdfReader
from pymongo import MongoClient
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()
pdf = open('../data/PA00TBCT.pdf', 'rb')
pdf_reader = PdfReader(pdf)

uri = "mongodb+srv://michael:XtDdgICBBjQtEUuX@nourish.optsg9l.mongodb.net/?retryWrites=true&w=majority&appName=Nourish"

# Create a new client and connect to the server
client = MongoClient(uri)

text = ""
for page in pdf_reader.pages:
    text += page.extract_text()

doc =  Document(page_content=text, metadata={"source": "PA00TBCT"})

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
    length_function=len
    )
docs = text_splitter.split_documents([doc])

dbName = "nutri_knowledge"
collectionName = "usaid_handbook"
collection = client[dbName][collectionName]

embeddings = OpenAIEmbeddings()

vectorStore = MongoDBAtlasVectorSearch.from_documents(docs, embeddings, collection=collection)