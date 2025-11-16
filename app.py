import gradio as gr
from sql_agent import create_sql_chain, ask_question

# Initialize the system once when app starts
print("Initializing SQL Query Buddy...")
db, vector_store, llm, memory = create_sql_chain()
print("Ready!")


def chat(user_message, history):
    """Process user message and return response."""

    if not user_message.strip():
        return history

    result = ask_question(db, vector_store, llm, memory, user_message)

    if "error" in result:
        response = f"❌ **Error:** {result['error']}"
    else:
        response = f"""**🔍 SQL Query:**
```sql
{result['sql_query']}
```

**📖 Explanation:**
{result['explanation']}

**📊 Results:**
```
{result['results']}
```

**💡 Insight:**
{result['insight']}

**🗂️ Tables Used:** {', '.join(result['tables_used'])}
"""

    history.append([user_message, response])
    return history


def clear_memory():
    """Clear conversation memory for fresh start."""
    global memory
    from langchain_community.chat_message_histories import ChatMessageHistory
    memory = ChatMessageHistory()
    return []


def use_example(example_text):
    """Return example text to be used in the input box."""
    return example_text


# Create the Gradio interface
with gr.Blocks(
    title="SQL Query Buddy",
    theme=gr.themes.Soft(),
    css="""
        .main-header {
            text-align: center;
            margin-bottom: 20px;
        }
        .feature-box {
            background: #f0f0f0;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
        }
    """
) as demo:

    # Header
    gr.Markdown("""
    <div class="main-header">

    # 🤖 SQL Query Buddy
    ### Conversational AI for Smart Data Insights

    *Ask questions about your database in natural language. I'll generate SQL, execute it, and provide insights!*

    </div>
    """)

    # Main chat interface
    chatbot = gr.Chatbot(
        height=450,
        show_label=False,
    )

    # Input area
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your question here... (e.g., 'Show me top customers by spending')",
            label="Your Question",
            scale=4
        )
        submit_btn = gr.Button("Ask", variant="primary", scale=1)

    # Control buttons
    with gr.Row():
        clear_chat = gr.Button("🗑️ Clear Chat", variant="secondary")
        clear_mem = gr.Button("🧠 Reset Memory", variant="secondary")

    # Example questions
    gr.Markdown("### 💡 Try These Examples:")

    with gr.Row():
        ex1 = gr.Button("Top 3 customers by spending", size="sm")
        ex2 = gr.Button("Revenue by product category", size="sm")
        ex3 = gr.Button("Monthly revenue trend", size="sm")

    with gr.Row():
        ex4 = gr.Button("Customers from California", size="sm")
        ex5 = gr.Button("Average order value", size="sm")
        ex6 = gr.Button("Products sold in January", size="sm")

    # Features info
    gr.Markdown("""
    ---
    ### ✨ Features:
    - **RAG-Powered** - Uses vector database for smart schema retrieval
    - **Context Memory** - Remembers previous questions for follow-ups
    - **AI Insights** - Analyzes results and finds patterns
    - **SQL Explanations** - Beginner-friendly query explanations
    """)

    # Database info
    with gr.Accordion("📁 Database Schema", open=False):
        gr.Markdown("""
        **Available Tables:**
        - **customers** - Customer info (name, email, region, signup_date)
        - **products** - Product catalog (name, category, price)
        - **orders** - Order records (customer_id, order_date, total_amount)
        - **order_items** - Line items (order_id, product_id, quantity, subtotal)
        """)

    # Event handlers
    msg.submit(chat, [msg, chatbot], chatbot)
    msg.submit(lambda: "", None, msg)

    submit_btn.click(chat, [msg, chatbot], chatbot)
    submit_btn.click(lambda: "", None, msg)

    clear_chat.click(lambda: [], None, chatbot)
    clear_mem.click(clear_memory, None, chatbot)

    # Example button handlers
    ex1.click(lambda: "What are the top 3 customers by total spending?", None, msg)
    ex2.click(lambda: "How much revenue did each product category generate?", None, msg)
    ex3.click(lambda: "Show the trend of monthly revenue over time", None, msg)
    ex4.click(lambda: "Show me all customers from California", None, msg)
    ex5.click(lambda: "Find the average order value", None, msg)
    ex6.click(lambda: "How many unique products were sold in January?", None, msg)

    # Footer
    gr.Markdown("""
    ---
    <center>
    Built with ❤️ using LangChain, FAISS, and Gradio | #CodecademyGenAIBootcamp
    </center>
    """)


# Launch the app
if __name__ == "__main__":
    demo.launch()
