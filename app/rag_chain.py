import os
from operator import itemgetter
from typing import TypedDict

from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnableParallel

load_dotenv()

vector_store = PGVector(
    collection_name="collection164",
    connection_string="postgresql+psycopg2://postgres:151102@localhost:5432/postgres",
    embedding_function=OpenAIEmbeddings()
)

template = """
Answer given the following context:
{context}

Question: {question}
"""

ANSWER_PROMPT = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(temperature=0, model='gpt-4-1106-preview', streaming=True)


class RagInput(TypedDict):
    question: str


final_chain = (
    RunnableParallel(
        context=(itemgetter("question") | vector_store.as_retriever()),
        question=itemgetter("question")
    ) |
    RunnableParallel(
        answer=(ANSWER_PROMPT | llm),
        docs=itemgetter("context")
    )
).with_types(input_type=RagInput)
