# 🤖 SQL Query Buddy

A conversational AI agent that converts natural language questions into SQL queries, executes them, and provides AI-driven insights.

Built with **LangChain**, **FAISS VectorDB**, and **Gradio** for the Codecademy GenAI & Agents Bootcamp Contest.

---

## 🎯 Features

- **Natural Language to SQL** - Ask questions in plain English, get accurate SQL queries
- **RAG-Powered** - Uses vector database to semantically search table schemas
- **SQL Explanations** - Beginner-friendly explanations of what each query does
- **AI Insights** - Analyzes query results and provides business insights
- **Conversation Memory** - Remembers context for follow-up questions
- **Clean Chat Interface** - Interactive Gradio UI for easy interaction

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Framework | LangChain |
| LLM | OpenAI GPT-3.5 |
| Vector Database | FAISS |
| Embeddings | OpenAI Embeddings |
| Database | SQLite |
| Frontend | Gradio |
| Language | Python 3.13 |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/sql-query-buddy.git
cd sql-query-buddy
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# OR
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install langchain langchain-openai langchain-community python-dotenv sqlalchemy faiss-cpu gradio
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Initialize the database

```bash
cd database
python setup_database.py
cd ..
```

---

## 🚀 Usage

### Run the application

```bash
python app.py
```

This will launch the Gradio interface in your browser.

### Example Questions

- "Show me all customers from California"
- "What are the top 3 customers by total spending?"
- "Which product category generates the most revenue?"
- "Show total sales per region for 2025"
- "How many unique products were sold in January?"
- "Show the trend of monthly revenue over time"
- "Find the average order value for returning customers"

---

## 🗄️ Database Schema

The project uses a retail commerce database with 4 tables:

**customers** - Customer information (name, email, region, signup date)

**products** - Product catalog (name, category, price)

**orders** - Order records (customer, date, total amount)

**order_items** - Line items (links orders to products with quantity)

---

## 🧠 How It Works

1. **User asks a question** in natural language

2. **Vector search** finds relevant table schemas from FAISS database

3. **LLM generates SQL** using the retrieved schema context

4. **Query executes** against the SQLite database

5. **AI analyzes results** and provides insights

6. **Conversation saved** to memory for follow-up questions

---

## 🔑 Key Components

### sql_agent.py

- `create_schema_documents()` - Creates searchable documents for each table
- `create_vector_store()` - Embeds schemas in FAISS vector database
- `get_relevant_schemas()` - Retrieves relevant tables based on question
- `ask_question()` - Main RAG pipeline: retrieve → generate → execute → insight

### app.py

- Gradio chat interface
- Integrates with sql_agent functions
- Displays SQL, results, and insights

---

## 👤 Author

**Rubin** - Software Engineer
Codecademy GenAI & Agents Bootcamp Participant

---

## 🏷️ Tags

#CodecademyGenAIBootcamp #RAG #LangChain #VectorDB #SQL #AI #Gradio
