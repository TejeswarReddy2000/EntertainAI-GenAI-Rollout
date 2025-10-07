import os
import gradio as gr
from dotenv import load_dotenv

# LangChain + Gemini
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

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

# 3. Use HuggingFace embeddings (no quota issues)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Build RAG pipeline from uploaded PDF
def build_qa_chain(pdf_file):
    loader = PyPDFLoader(pdf_file.name)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
    )
    return qa_chain

# 5. Gradio UI
with gr.Blocks(title="🎬 Sponsor Dashboard: Movie Insights") as demo:
    gr.Markdown("## 🎬 Sponsor Dashboard\nUpload a movie-related PDF and ask questions about its content.")
    file = gr.File(label="Upload PDF", file_types=[".pdf"])
    chatbot = gr.Chatbot(height=400, type="messages")
    msg = gr.Textbox(placeholder="Ask a question about the uploaded document...")
    clear = gr.Button("Clear")

    qa_chain = None

    def load_file(f):
        global qa_chain
        qa_chain = build_qa_chain(f)
        return [{"role": "assistant", "content": "✅ File loaded. You can now ask questions about the document."}]

    def answer_query(user, history):
        if qa_chain is None:
            return history + [
                {"role": "user", "content": user},
                {"role": "assistant", "content": "⚠️ Please upload a PDF first."}
            ], ""
        result = qa_chain.invoke({"query": user})
        answer = result["result"]
        sources = result.get("source_documents", [])
        source_texts = "\n\n".join([doc.page_content[:300] + "..." for doc in sources[:2]])
        full_reply = f"{answer}\n\n📄 Source Snippets:\n{source_texts}" if sources else answer
        return history + [
            {"role": "user", "content": user},
            {"role": "assistant", "content": full_reply}
        ], ""

    file.upload(load_file, file, chatbot)
    msg.submit(answer_query, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot, queue=False)

# 6. Launch
if __name__ == "__main__":
    demo.launch()
