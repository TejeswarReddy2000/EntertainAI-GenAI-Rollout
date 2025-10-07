import os
import gradio as gr
from dotenv import load_dotenv

# LangChain + Gemini
from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings  # ✅ Local embeddings

# 1. Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("⚠️ Please set GEMINI_API_KEY in your .env file")

# 2. Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-pro-latest",
    google_api_key=api_key,
    temperature=0.2,
)

# 3. Load PDF dataset
base_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(base_dir, "data", "Jathi_rathanalu_censor_script_telugu.pdf")

print("📂 Using PDF path:", pdf_path)

loader = PyPDFLoader(pdf_path)
docs = loader.load()
print("✅ Loaded", len(docs), "documents")

# 4. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# 5. HuggingFace Embeddings (no Google quota)
print("🔍 Using HuggingFace embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 6. Create FAISS vector DB
print("🗂️ Building FAISS index...")
vectorstore = FAISS.from_documents(chunks, embeddings)

# 7. RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
    verbose=True,
)

# 8. Chat function
def chat(query, history):
    result = qa.invoke({"query": query})
    return result["result"]

# 9. Gradio UI
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask me about the Jathi Ratnalu script...")
    clear = gr.Button("Clear")

    def respond(user, history):
        bot_reply = chat(user, history)
        history = history + [(user, bot_reply)]
        return history, ""

    msg.submit(respond, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot, queue=False)

# 10. Run app
if __name__ == "__main__":
    demo.launch()

