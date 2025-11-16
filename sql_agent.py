from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()


# Configurations
DB_PATH = "database/retail_commerce.db"
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0


# Create Schema Documents for Vector DB
def create_schema_documents(db):
    tables = db.get_usable_table_names()

    table_descriptions = {
        "customers": "Customer information including name, email, region/location, and signup date. Use this table for queries about customers, users, buyers, clients, or people who make purchases.",
        "products": "Product catalog with product names, categories (Electronics, Furniture, Accessories), and prices. Use this for queries about items, merchandise, inventory, or what is being sold.",
        "orders": "Order records showing which customers made a purchase, when (order_date), and the total amount. Use this for queries about purchases, transactions, sales, or revenue.",
        "order_items": "Line items within each order - links orders to products with quantity and subtotal. Use this for queries about what products were in an order, quantities sold, or detailed purchase breakdowns.",
    }

    documents = []

    for table in tables:
        schema_info = db.get_table_info([table])

        content = f"""
TABLE: {table}

BUSINESS CONTEXT:
{table_descriptions.get(table, "No description available.")}

SCHEMA AND SAMPLE DATA:
{schema_info}
"""

        doc = Document(page_content=content, metadata={"table_name": table})

        documents.append(doc)

    return documents


# Create Vector Database
def create_vector_store(documents):
    embedding = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embedding)
    return vector_store


# Retrieve Relevant Schemas
def get_relevant_schemas(vector_store, questions, k=4):
    relevant_docs = vector_store.similarity_search(questions, k=k)
    schemas = "\n\n".join([doc.page_content for doc in relevant_docs])
    selected_tables = [doc.metadata["table_name"] for doc in relevant_docs]
    return schemas, selected_tables


# SQL Generation With RAG
def create_sql_chain():
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
    documents = create_schema_documents(db)
    vector_store = create_vector_store(documents)
    llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)
    memory = ChatMessageHistory()
    return db, vector_store, llm, memory


def ask_question(db, vector_store, llm, memory, question):
    relevant_schemas, selected_tables = get_relevant_schemas(vector_store, question)
    chat_history = memory.messages
    history_text = ""
    if chat_history:
        history_text = "\n".join([f"{msg.type}: {msg.content}" for msg in chat_history])

    prompt = f"""You are a SQL expert.  Based on the table schemas below, write a SQL query to answer the user's question.

    RELEVANT TABLE SCHEMAS:
    {relevant_schemas}

    CONVERSATION HISTORY:
    {history_text if history_text else "No previous conversation."}

    USER QUESTION:
    {question}

    Instructions:
    1. Write a valid SQLite query
    2. Use only the tables and columns shown in the schemas above
    3. If the question references previous results (like "those", "them", "filter"), use the conversation history
    4. Return ONLY the SQL query, no explanations or additional text.

    SQL QUERY:"""

    print("\n🤖 Generating SQL...")
    response = llm.invoke(prompt)
    sql_query = response.content.strip()

    if sql_query.startswith("```"):
        sql_query = sql_query.split("\n", 1)[1]
    if sql_query.endswith("```"):
        sql_query = sql_query.rsplit("```", 1)[0]
    sql_query = sql_query.strip()

    try:
        results = db.run(sql_query)
        print(f"\n📊 Results:\n{results}")

        insight_prompt = f"""Based on this query result, give a 1 - 2 sentence insight:
        QUERY RESULT: {sql_query}
        RESULTS: {results}
        Insight:"""

        insight_response = llm.invoke(insight_prompt)
        insight = insight_response.content.strip()
        print(f"\n💡 Insight:\n{insight}")

        memory.add_message(HumanMessage(content=question))
        memory.add_message(AIMessage(content=f"SQL: {sql_query}\nResults: {results}"))

        return {
            "sql_query": sql_query,
            "results": results,
            "insight": insight,
            "tables_used": selected_tables,
        }

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return {"error": str(e)}


# Main execution
if __name__ == "__main__":
    print("SQL QUERY BUDDY")

    # Setup
    db, vector_store, llm, memory = create_sql_chain()

    # Test queries
    ask_question(db, vector_store, llm, memory, "Show me all customers from California")

    ask_question(
        db, vector_store, llm, memory, "What are the top 3 customers by total spending?"
    )

    ask_question(
        db,
        vector_store,
        llm,
        memory,
        "What products did the top customer buy and which customer is it?",
    )
