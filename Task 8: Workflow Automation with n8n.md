
Perfect 👍 You’re now at **Task 8 — Workflow Automation (n8n Integration)**

Here’s a complete and beginner-friendly **`README.md`** you can directly use in your **Task_8_Workflow_Automation** folder on GitHub 👇

---

### 📘 README.md

#### 🧩 **Task 8 — Workflow Automation with n8n**

##### **1. Objective**

The goal of this task is to **automate workflows** that connect multiple tools such as **Slack**, **Gmail**, and **webhooks** using **n8n** — a no-code/low-code automation platform.

This allows automatic alerts, notifications, or actions based on specific conditions (for example, sending an email if a rating is low or notifying a Slack channel when sales are high).

---

##### **2. Description**

This workflow automates data handling and alerting without manual effort.
For example:

* If a show’s **rating < 3** and **ticket sales > 90**, send a Slack alert to the content team.
* If **client investment > 50**, send a Gmail update to the finance team.

The automation uses an **n8n workflow** that starts with a **Webhook Trigger**, processes data through an **IF node**, and executes different actions accordingly.

---

##### **3. Step-by-Step Workflow Setup**

#### 🧩 **Step 1 — Start n8n**

1. Open n8n in your browser (e.g., [http://localhost:5678](http://localhost:5678))
2. Click **“+ New Workflow”**

---

#### ⚙️ **Step 2 — Add Webhook Trigger**

1. Drag a **Webhook node** as the first node.
2. Set:

   * **HTTP Method:** `POST`
   * **Path:** e.g., `langchain_task8`
3. Copy the generated webhook URL (it looks like:

   ````
   http://localhost:5678/webhook-test/langchain_task8
   ```)

   ````
4. Save and **Activate Workflow**.

---

#### 📩 **Step 3 — Send Test Data to Webhook**

Use **Postman** or another tool to send a `POST` request to the webhook URL.
Example JSON data:

```json
{
  "rating": 2,
  "ticket_sales": 95,
  "client_investment": 75
}
```

If successful, n8n will show the data inside the webhook node.

---

#### ⚖️ **Step 4 — Add IF Node (Condition Check)**

1. Add an **IF Node** after the Webhook.

2. Create these conditions:

   | Field                            | Operation    | Value |
   | -------------------------------- | ------------ | ----- |
   | `{{$json["rating"]}}`            | less than    | 3     |
   | `{{$json["ticket_sales"]}}`      | greater than | 90    |
   | `{{$json["client_investment"]}}` | greater than | 50    |

3. This ensures that the next actions run **only if all conditions are true**.

---

#### 💬 **Step 5 — Add Slack Node**

1. On the **True** output of IF → Add a **Slack node**.
2. Configure Slack API credentials.
3. Choose **“Send Message to Channel.”**
4. Write a message like:

   ```
   ⚠️ Alert: Low rating but high sales detected!
   Rating: {{$json["rating"]}}
   Ticket Sales: {{$json["ticket_sales"]}}
   Client Investment: {{$json["client_investment"]}}
   ```

---

#### 📧 **Step 6 — Add Gmail Node (Optional)**

1. On the **True** branch (after Slack), add a **Gmail node.**
2. Set:

   * **To:** your test email
   * **Subject:** "Alert – Review Performance"
   * **Body:**

     ```
     Alert Summary:
     Rating: {{$json["rating"]}}
     Ticket Sales: {{$json["ticket_sales"]}}
     Client Investment: {{$json["client_investment"]}}
     ```

---

#### 🧠 **Step 7 — Test and Execute**

1. Run the workflow.
2. Send JSON data again via Postman.
3. If the conditions are met:

   * Slack receives an alert.
   * Gmail receives an email notification.

---

##### **4. Example Workflow Diagram**

```
Webhook (POST) 
   ↓
IF Node (Check Conditions)
   ↓
Slack Message → Gmail Notification
```

---

##### **5. Example JSON Input**

```json
[
  {"rating": 2, "ticket_sales": 95, "client_investment": 75},
  {"rating": 4, "ticket_sales": 80, "client_investment": 60},
  {"rating": 1, "ticket_sales": 92, "client_investment": 70}
]
```

Each entry can trigger or skip alerts based on the conditions.

---

##### **6. Key Takeaway**

This workflow demonstrates **intelligent automation** using **n8n**, allowing data-driven decisions and alerts without coding.
It connects APIs, evaluates conditions, and triggers actions in **real time**.

---



<img width="1920" height="1080" alt="Screenshot (175)" src="https://github.com/user-attachments/assets/3b59db87-4bae-4ef4-b2fd-e38048572bd3" />

