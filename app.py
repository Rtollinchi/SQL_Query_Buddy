import gradio as gr
from sql_agent import create_sql_chain, ask_question

# Initialize the system once when app starts
print("Initializing SQL Query Buddy...")
db, vector_store, llm, memory = create_sql_chain()
print("Ready!")


def chat(user_message, history):

    # Call ask_question function
    result = ask_question(db, vector_store, llm, memory, user_message)

    # Format the response
    if "error" in result:
        response = f"❌ Error: {result['error']}"
    else:
        response = f"""**SQL Query:**
```sql
{result['sql_query']}
```

**Results:**
{result['results']}

**Insight:**
{result['insight']}

**Tables Used:** {', '.join(result['tables_used'])}
"""

    # Add to history
    history.append([user_message, response])

    return history


# Create the Gradio interface
with gr.Blocks(title="SQL Query Buddy") as demo:
    gr.Markdown("# 🤖 SQL Query Buddy")
    gr.Markdown("Ask questions about your database in natural language!")

    chatbot = gr.Chatbot(height=500)

    msg = gr.Textbox(
        placeholder="Ask a question like: 'Show me top 5 customers by spending'",
        label="Your Question"
    )

    clear = gr.Button("Clear Chat")

    # When user submits a message
    msg.submit(chat, [msg, chatbot], chatbot)
    msg.submit(lambda: "", None, msg)  # Clear input box

    # Clear button resets chat
    clear.click(lambda: [], None, chatbot)

    # Example questions
    gr.Markdown("### Example Questions:")
    gr.Markdown("""
    - Show me all customers from California
    - What are the top 3 customers by total spending?
    - Which product category generates the most revenue?
    - What products did the top customer purchase?
    """)


# Launch the app
if __name__ == "__main__":
    demo.launch()
