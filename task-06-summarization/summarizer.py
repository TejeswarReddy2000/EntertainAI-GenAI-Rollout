import os
import re
import gradio as gr
from dotenv import load_dotenv

# Gemini + LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# PDF/Text handling
import PyPDF2
import google.generativeai as genai

# --------------------------
# 1️⃣ Load API Key
# --------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("⚠️ Please set GEMINI_API_KEY in your .env file")

# --------------------------
# 2️⃣ Configure Gemini & Select Model
# --------------------------
genai.configure(api_key=api_key)
models_list = list(genai.list_models())
model_name = next(
    (m.name for m in models_list if "gemini-pro" in m.name and "generateContent" in m.supported_generation_methods),
    models_list[0].name
)

# --------------------------
# 3️⃣ Gemini LLM for LangChain
# --------------------------
llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)

# --------------------------
# 4️⃣ Text Extraction
# --------------------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    else:
        text = file.read().decode("utf-8")
    return text

# --------------------------
# 5️⃣ Chunking
# --------------------------
def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents([Document(page_content=text)])

# --------------------------
# 6️⃣ Summarization Engine
# --------------------------
def summarize(text, strategy):
    chunks = chunk_text(text)
    chain_type = "map_reduce" if strategy == "MapReduce" else "refine"
    chain = load_summarize_chain(llm, chain_type=chain_type, verbose=True)
    summary = chain.run(chunks)
    return summary

# --------------------------
# 7️⃣ Gradio UI
# --------------------------
with gr.Blocks(title="📝 Gemini Summarization Engine") as demo:
    gr.Markdown("## 📝 Gemini Summarization Engine\nUpload a document and choose a strategy.")
    file = gr.File(label="📄 Upload PDF or Text", file_types=[".pdf", ".txt"])
    strategy = gr.Radio(["MapReduce", "Refine"], label="🧠 Strategy", value="MapReduce")
    btn = gr.Button("Summarize")
    output = gr.Textbox(label="📝 Summary", lines=15)
    clear = gr.Button("Clear")

    def run_summary(f, s):
        if not f:
            return "⚠️ Please upload a file."
        try:
            text = extract_text(f)
            return summarize(text, s)
        except Exception as e:
            return f"⚠️ Summarization failed: {str(e)}"

    btn.click(run_summary, [file, strategy], output)
    clear.click(lambda: "", None, output)

# --------------------------
# 8️⃣ Launch
# --------------------------
if __name__ == "__main__":
    demo.launch()
