### 📘 README.md

#### 🧩 **Task 1: Chatbot with Memory**

##### **1. Description**

This task implements a simple **AI chatbot** that can remember previous messages during a conversation. It uses **LangChain** and an **LLM (Large Language Model)** to respond naturally while maintaining context from earlier interactions.

##### **2. Logic**

1. **User Input:** The user sends a message (e.g., "Hello, how are you?").
2. **Memory Retrieval:** The system checks previous messages from the same chat session.
3. **Response Generation:** The model combines the user’s new message and previous context to generate a coherent reply.
4. **Memory Update:** The chatbot stores the latest message and response for use in future turns.

##### **3. Flow Diagram**

```
User Input → Retrieve Memory → Combine Context + New Message 
→ Generate Response → Display → Save to Memory
```

##### **4. Memory Type Used**

* **ConversationBufferMemory**

  * Stores the entire conversation history as a text buffer.
  * Suitable for simple chatbots where the model needs to “see” the previous dialogue for continuity.
  * Example:

    ```python
    from langchain.memory import ConversationBufferMemory
    memory = ConversationBufferMemory()
    ```
  * This memory keeps all past messages in sequence and provides them to the LLM during response generation.

##### **5. Example Behavior**

```
User: Hello!
Bot: Hi there! How can I help you today?

User: Who are you?
Bot: I'm your friendly chatbot. You just greeted me a moment ago!
```

##### **6. Key Takeaway**

This chatbot demonstrates **short-term conversational memory** using LangChain’s **ConversationBufferMemory**, allowing it to maintain simple context awareness in a single session.


<img width="1920" height="1080" alt="Screenshot (168)" src="https://github.com/user-attachments/assets/fffe8017-883a-4c28-840d-f5a93417ac24" />
