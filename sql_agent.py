from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.documents import Document

load_dotenv()


# Configurations
DB_PATH = "database/retail_commerce.db"
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0


# Create Schema Documents for Vector DB
def create_schema_documents(db):
    tables = db.get_usable_names()

    table_descriptions = {
        "customers": "Customer information including name, email, region/location, and signup date. Use this table for queries about customers, users, buyers, clients, or people who make purchases.",
        "products": "Product catalog with product names, categories (Electronics, Furniture, Accessories), and prices. Use this for queries about items, merchandise, inventory, or what is being sold.",
        "orders": "Order records showing which customers made a purchase, when (order_date), and the total amount. Use this for queries about purchases, transactions, sales, or revenue.",
        "order_items": "Line items within each order - links orders to products with quantity and subtotal. Use this for queries about what products were in an order, quantities sold, or detailed purchase breakdowns."
    }

    documents = []

    for table in tables:
        schema_info = db.get_table_info(table)

        content = f"""
TABLE: {table}

BUSINESS CONTEXT:
{table_descriptions.get(table, "No description available.")}

SCHEMA AND SAMPLE DATA:
{schema_info}
"""

        doc = Document(
            page_content=content,
            metadata={"table_name": table}
        )

        documents.append(doc)

    return documents


# Create Vector Database
def create_vector_store(documents):
    embedding = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embedding)
    return vector_store


# Retrieve Relevant Schemas
def get_relevant_schemas(vector_store, questions, k=2):
    relevant_docs = vector_store.similarity_search(questions, k=k)
    schemas = "\n\n".join([doc.page_content for doc in relevant_docs])
    selected_tables = [doc.metadata["table_name"] for doc in relevant_docs]
    return schemas, selected_tables


# SQL Generation With RAG
def create_sql_chain():
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
    documents = create_schema_documents(db)
    vector_store = create_vector_store(documents)
    llm = ChatOpenAI(model_name=MODEL_NAME, temperature=TEMPERATURE)
    memory = ChatMessageHistory()
    return db, vector_store, llm, memory
