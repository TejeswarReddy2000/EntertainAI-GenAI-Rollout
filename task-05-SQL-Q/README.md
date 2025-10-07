
---

### 📘 README.md

#### 🧩 **Task 5 — Chatbot with Combined Memory (Hybrid Memory System)**

##### **1. Description**

This task creates an **advanced AI chatbot** that combines **conversational memory** and **knowledge-based memory**.
It can **remember the current chat context** while also **retrieving factual information** from an external knowledge base.

This hybrid setup makes the chatbot both **context-aware** (knows the flow of conversation) and **knowledgeable** (knows real information).

---

##### **2. Logic**

1. **Conversation Memory:**
   Stores recent dialogue so the chatbot can maintain context (like who said what).

2. **Vector Memory (Knowledge Base):**
   Stores factual or reference data (e.g., about AI, company policies, etc.) as embeddings in a vector database.

3. **Hybrid Workflow:**

   * When a user asks a question, the chatbot uses **conversation memory** to understand the context.
   * It simultaneously searches the **vector memory** to retrieve relevant knowledge.
   * The two are combined and sent to the **LLM** to generate a meaningful and contextually accurate response.

---

##### **3. Flow Diagram**

```
User Input
   ↓
Retrieve Conversation Context (short-term)
   ↓
Search Vector Store for Relevant Knowledge (long-term)
   ↓
Combine Both Contexts
   ↓
Generate Response via LLM
   ↓
Display Answer
   ↓
Update Both Memories
```

---

##### **4. Memory Types Used**

**a) ConversationBufferMemory**

* Maintains short-term memory of recent chat exchanges.
* Example:

  ```python
  from langchain.memory import ConversationBufferMemory
  short_term = ConversationBufferMemory()
  ```

**b) VectorStoreRetrieverMemory**

* Provides long-term memory through semantic search on embedded data.
* Example:

  ```python
  from langchain.memory import VectorStoreRetrieverMemory
  from langchain.vectorstores import FAISS
  from langchain.embeddings import OpenAIEmbeddings

  embeddings = OpenAIEmbeddings()
  vectorstore = FAISS.from_texts(["AI automates human-like tasks"], embeddings)
  retriever = vectorstore.as_retriever()
  long_term = VectorStoreRetrieverMemory(retriever=retriever)
  ```

Together, they form a **hybrid memory** system that supports both **context retention** and **knowledge recall**.

---

##### **5. Example Behavior**

```
User: Hi, I’m learning about AI. What can it do?
Bot: AI can perform tasks like speech recognition, image analysis, and decision-making.

User: Remind me what I said earlier?
Bot: You mentioned you’re learning about AI.
```

The bot remembers your earlier message (via conversation memory)
and gives factual answers (via vector memory).

---

##### **6. Key Takeaway**

This chatbot demonstrates a **hybrid memory system** that combines:

* **Short-term memory** for maintaining conversation flow, and
* **Long-term memory** for retrieving factual or document-based knowledge.

This setup is ideal for **intelligent assistants**, **knowledge bots**, or **customer support systems** that must handle both chat context and stored information efficiently.

---
<img width="1920" height="1080" alt="Screenshot (173)" src="https://github.com/user-attachments/assets/6f158168-9377-497d-9f9a-2ac562da7439" />
