import os
import sys
print(sys.path)
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

load_dotenv()

loader = DirectoryLoader(
    os.path.abspath(
        "E:/FILE of Trong/LLMs/retrieval_augmented_generation_project/danang_trip_assisstant/pdf-documents"),
    glob="**/*.pdf",
    use_multithreading=True,
    show_progress=True,
    max_concurrency=50,
    loader_cls=UnstructuredPDFLoader,
)
docs = loader.load()

embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', )

text_splitter = SemanticChunker(
    embeddings=embeddings
)

flattened_docs = [Document(page_content=doc.page_content)
                  for doc in docs if doc.page_content]
chunks = text_splitter.split_documents(flattened_docs)

PGVector.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="collection164",
    connection_string="postgresql+psycopg2://postgres:151102@localhost:5432/postgres",
    pre_delete_collection=True,
)
