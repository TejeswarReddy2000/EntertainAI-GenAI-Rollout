import os
import gradio as gr
from dotenv import load_dotenv
import uuid

# Google Generative AI and LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
from langchain_core.runnables.history import RunnableWithMessageHistory

# Use the correct import for InMemoryChatMessageHistory
try:
    from langchain_core.chat_history import InMemoryChatMessageHistory
except ImportError:
    try:
        from langchain.memory import InMemoryChatMessageHistory
    except ImportError:
        raise ImportError("InMemoryChatMessageHistory not found. Please upgrade your langchain packages.")

# 1. Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("⚠️ Please set GEMINI_API_KEY in your .env file")

# 2. Initialize Gemini LLM (replace with a supported model name if needed)
llm = ChatGoogleGenerativeAI(
    model="models/gemini-pro-latest",  # <-- Supported model from your list
    google_api_key=api_key,
    temperature=0.2,
)

# 3. Add memory to chatbot (latest LangChain API)
def get_session_history(session_id):
    if not hasattr(get_session_history, "histories"):
        get_session_history.histories = {}
    if session_id not in get_session_history.histories:
        get_session_history.histories[session_id] = InMemoryChatMessageHistory()
    return get_session_history.histories[session_id]

conversation = RunnableWithMessageHistory(
    runnable=llm,
    get_session_history=get_session_history,
    verbose=True,
)

# 4. Define chatbot function
def chat(user_input: str, session_id: str) -> str:
    response = conversation.invoke(
        input=user_input,
        config={"configurable": {"session_id": session_id}}
    )
    return response

# 5. Gradio UI
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type='messages')
    msg = gr.Textbox(placeholder="Ask me about movies...")
    clear = gr.Button("Clear Chat")
    session_id_state = gr.State(str(uuid.uuid4()))

    def respond(user, history, session_id):
        bot_reply = chat(user, session_id)
        if not isinstance(bot_reply, str):
            bot_reply = str(bot_reply)
        import re
        # Replace all double newlines with a single newline
        bot_reply = re.sub(r'\n{2,}', '\n', bot_reply)
        # Add a newline before each bullet point movie entry
        bot_reply = re.sub(r'(?<!\n)(\*\s)', r'\n\1', bot_reply)
        # Add a newline before each movie title with year (e.g., Movie Name (2018))
        bot_reply = re.sub(r'(?<!\n)([A-Za-z0-9 ,\-]+\(\d{4}\))', r'\n\1', bot_reply)
        # Add a newline before each movie title with colon (e.g., Movie Name:)
        bot_reply = re.sub(r'(?<!\n)([A-Za-z0-9 ,\-]+:)', r'\n\1', bot_reply)
        history = history + [
            {"role": "user", "content": user},
            {"role": "assistant", "content": bot_reply}
        ]
        return history, ""

    msg.submit(respond, [msg, chatbot, session_id_state], [chatbot, msg])
    clear.click(lambda: [], None, chatbot, queue=False)

# 6. Launch app
if __name__ == "__main__":
    demo.launch()