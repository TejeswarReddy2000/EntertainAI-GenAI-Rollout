

---

### 📘 README.md

#### 🧩 **Task 2 — Chatbot with Conversation Summary Memory**

##### **1. Description**

This task builds upon Task 1 by adding a **summary-based memory** to the chatbot.
Instead of storing the full chat history, the system keeps a **short summary** of previous interactions.
This helps maintain context while using **less memory**, making it suitable for **long conversations**.

##### **2. Logic**

1. **User sends a message.**
2. **Memory retrieves a summarized version** of the past conversation.
3. **LLM uses this summary + new input** to generate a contextual response.
4. **Memory updates automatically** by summarizing the new exchange and storing it.

##### **3. Flow Diagram**

```
User Input 
   ↓
Retrieve Summarized Memory 
   ↓
Combine Summary + Current Message 
   ↓
Generate Response via LLM 
   ↓
Display Response 
   ↓
Update Summary in Memory
```

##### **4. Memory Type Used**

* **ConversationSummaryMemory**

  * Uses an LLM to **summarize previous dialogue** after each turn.
  * Keeps the essential context while discarding unnecessary details.
  * Ideal for **long-running chat sessions** or **resource-limited systems**.
  * Example:

    ```python
    from langchain.memory import ConversationSummaryMemory
    memory = ConversationSummaryMemory(llm=chat_model)
    ```
  * The summary is stored and refreshed automatically as the conversation continues.

##### **5. Example Behavior**

```
User: Hello! Yesterday we talked about AI projects.
Bot: Yes, I remember you’re working on an AI project. How’s it going today?

User: It’s going great, I added a recommendation system.
Bot: That’s awesome! What type of recommendations are you building?
```

##### **6. Key Takeaway**

This chatbot demonstrates how to maintain **long-term conversational context** efficiently using **ConversationSummaryMemory**, which balances **context retention** and **performance**.

---

<img width="1920" height="1080" alt="Screenshot (169)" src="https://github.com/user-attachments/assets/0973ff7e-0d59-43ac-ab86-04f8798e56ea" /><img width="1920" height="1080" alt="Screenshot (170)" src="https://github.com/user-attachments/assets/89b70a07-9fce-4390-aab9-93b79d165c31" />

