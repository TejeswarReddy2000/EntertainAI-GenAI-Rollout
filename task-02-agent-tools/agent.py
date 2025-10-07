import os
import gradio as gr
from dotenv import load_dotenv
from pydantic import BaseModel

# LangChain + Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool

# LangGraph
from langgraph.graph import StateGraph, END

# 1. Load Gemini API key securely
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("⚠️ Please set GEMINI_API_KEY in your .env file")

# 2. Initialize Gemini Pro
llm = ChatGoogleGenerativeAI(
    model="models/gemini-pro-latest",
    google_api_key=api_key,
    temperature=0.2,
)

# 3. Define LangChain tools
def ticket_tool(query: str) -> str:
    if "avatar" in query.lower():
        return "🎟️ Tickets for Avatar available at 6 PM, 8 PM, and 10 PM."
    elif "movie x" in query.lower():
        return "🎟️ Tickets for Movie X available at 7 PM and 9 PM."
    return "❌ No ticket info found."

def box_office_tool(query: str) -> str:
    prompt = f"Search online and summarize the latest box office forecast for: {query}. Include trends and expected earnings."
    response = llm.invoke(prompt)
    return response.content

def movie_info_tool(query: str) -> str:
    prompt = f"Search online and summarize key facts, plot, or cast details about: {query}. Include recent updates if available."
    response = llm.invoke(prompt)
    return response.content

def fallback_tool(query: str) -> str:
    return "🤖 I can help with ticket info, box office predictions, or movie facts. Try asking about those!"

tools = [
    Tool(name="TicketTool", func=ticket_tool, description="Check ticket availability"),
    Tool(name="BoxOfficeTool", func=box_office_tool, description="Predict box office revenue"),
    Tool(name="MovieInfoTool", func=movie_info_tool, description="Answer general movie questions"),
    Tool(name="FallbackTool", func=fallback_tool, description="Handle unmatched queries")
]

# 4. Define agent state
class AgentState(BaseModel):
    input: str
    output: str = ""

# 5. Routing logic
def route(state):
    query = state.input.lower()
    if "ticket" in query or "showtime" in query or "timing" in query:
        return "ticket_node"
    elif "box office" in query or "predict earnings" in query or "how much will" in query or "budget" in query or "collection" in query:
        return "box_office_node"
    elif "movie" in query or "about" in query or "who directed" in query or "plot" in query or "cast" in query or "avatar" in query:
        return "movie_info_node"
    else:
        return "fallback_node"

# 6. Node definitions
def ticket_node(state):
    result = tools[0].func(state.input)
    return {"output": result}

def box_office_node(state):
    result = tools[1].func(state.input)
    return {"output": result}

def movie_info_node(state):
    result = tools[2].func(state.input)
    return {"output": result}

def fallback_node(state):
    result = tools[3].func(state.input)
    return {"output": result}

def entry_node(state):
    return state

# 7. Build LangGraph agent
graph = StateGraph(AgentState)
graph.add_node("entry", entry_node)
graph.add_node("ticket_node", ticket_node)
graph.add_node("box_office_node", box_office_node)
graph.add_node("movie_info_node", movie_info_node)
graph.add_node("fallback_node", fallback_node)

graph.add_conditional_edges("entry", route, {
    "ticket_node": "ticket_node",
    "box_office_node": "box_office_node",
    "movie_info_node": "movie_info_node",
    "fallback_node": "fallback_node"
})

graph.add_edge("ticket_node", END)
graph.add_edge("box_office_node", END)
graph.add_edge("movie_info_node", END)
graph.add_edge("fallback_node", END)
graph.set_entry_point("entry")
agent = graph.compile()

# 8. Gradio UI
with gr.Blocks(title="🎬 EntertainAI GenAI Agent") as demo:
    gr.Markdown("## 🎬 EntertainAI GenAI Agent\nAsk about tickets, box office, or movie facts.")
    chatbot = gr.Chatbot(height=400)  # Enlarged output box
    dropdown = gr.Dropdown(
        choices=[
            "Ticket timings for Avatar",
            "Box office prediction for Jawan this weekend",
            "Who directed Titanic?",
            "Plot of Inception",
            "Budget of Avatar"
        ],
        label="🎯 Choose a sample query or type your own below",
        interactive=True
    )
    msg = gr.Textbox(placeholder="Or type your own question here...")
    clear = gr.Button("Clear")

    def handle_query(user_input):
        response = agent.invoke({"input": user_input})
        print("DEBUG:", response)
        if hasattr(response, "output"):
            return response.output or "🤖 I couldn't understand that."
        return response.get("output", "🤖 I couldn't understand that.")

    def respond(choice, history):
        if choice:
            reply = handle_query(choice)
            history = history + [(choice, reply)]
        return history, ""

    dropdown.change(respond, [dropdown, chatbot], [chatbot, dropdown])
    msg.submit(lambda x, h: (h + [(x, handle_query(x))], ""), [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot, queue=False)

# 9. Launch app
if __name__ == "__main__":
    demo.launch()
