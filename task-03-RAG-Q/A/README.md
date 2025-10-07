

### 📘 README.md

#### 🧩 **Task 3 — Chatbot with ConversationBufferWindowMemory**

##### **1. Description**

This task enhances the chatbot by introducing a **window-based memory system**.
Instead of remembering the *entire conversation* or a *summary*, the chatbot now remembers **only the last few interactions (window)**.

This helps the model stay focused on **recent context** without becoming overloaded by older data — useful for **real-time or fast-changing conversations**.

---

##### **2. Logic**

1. **User sends a new message.**
2. **Memory retrieves only the last few messages** (as defined by the window size).
3. **The LLM uses this limited context** to generate a relevant response.
4. **Older messages are automatically dropped** once the memory exceeds the window size.
5. **The latest exchange** is stored for the next turn.

---

##### **3. Flow Diagram**

```
User Input
   ↓
Retrieve Last N Messages (Window)
   ↓
Combine with New Message
   ↓
Generate Response via LLM
   ↓
Display Response
   ↓
Update Window Memory (Remove Oldest if Needed)
```

---

##### **4. Memory Type Used**

* **ConversationBufferWindowMemory**

  * Keeps only the **last N exchanges** (e.g., last 3 messages).
  * Old messages are discarded to keep memory small and efficient.
  * Ideal for **short-term focus** chatbots like support bots or task assistants.
  * Example:

    ```python
    from langchain.memory import ConversationBufferWindowMemory
    memory = ConversationBufferWindowMemory(k=3)
    ```

    Here, `k=3` means the chatbot remembers the **last 3 message pairs** (user + bot).

---

##### **5. Example Behavior**

```
User: Hi!
Bot: Hello there!

User: What’s your name?
Bot: I’m your chatbot assistant.

User: What did I say first?
Bot: You said “Hi!”

User: What did we talk about before that?
Bot: Sorry, I can only remember the last few messages.
```

---

##### **6. Key Takeaway**

This chatbot demonstrates **short-term conversational memory** using
`ConversationBufferWindowMemory`, which helps maintain **recent context** efficiently
without overloading the model with old data.

<img width="1920" height="1080" alt="Screenshot (171)" src="https://github.com/user-attachments/assets/650565fd-8a29-4d14-937a-d7ba086aa285" />

---

Would you like me to create similar `README.md` files for **Task 4 and Task 5** too (they usually cover VectorStoreMemory or Knowledge-based memory)?
