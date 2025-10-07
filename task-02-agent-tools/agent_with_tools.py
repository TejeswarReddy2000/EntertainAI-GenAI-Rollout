import os
import gradio as gr
from dotenv import load_dotenv

# Gemini LLM
from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore

# LangGraph
from langgraph.prebuilt import create_react_agent

# LangChain Tools
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
import numexpr


# 1. Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("⚠️ Please set GEMINI_API_KEY in your .env file")

# 2. Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="models/gemini-pro-latest",
    google_api_key=api_key,
    temperature=0.2,
)

# 3. Define tools
# Wikipedia search
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
# DuckDuckGo web search
duckduck = DuckDuckGoSearchRun()

# Calculator using numexpr
def calculator_tool(query: str) -> str:
    try:
        return str(numexpr.evaluate(query))
    except Exception as e:
        return f"Error: {e}"

calc = Tool(
    name="Calculator",
    func=calculator_tool,
    description="Evaluate math expressions (e.g., 2+2, 45*3, sqrt(16)).",
)

# List of tools
tools = [wiki, duckduck, calc]

# 4. Create AI Agent with LangGraph
agent = create_react_agent(llm, tools)

# 5. Gradio UI
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask me anything... (can search Wikipedia, web, or calculate)")
    clear = gr.Button("Clear")

    def respond(user, history):
        bot_reply = agent.invoke({"messages": [("user", user)]})
        reply_text = bot_reply["messages"][-1].content
        history = history + [(user, reply_text)]
        return history, ""

    msg.submit(respond, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot, queue=False)

# 6. Run app

if __name__ == "__main__":
    demo.launch()
