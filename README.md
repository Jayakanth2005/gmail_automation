# 📧 Gmail Rule-Based Email Processor  

🚀 **Gmail Rule-Based Email Processor** is an intelligent email automation system that fetches emails via the **Gmail API**, applies **custom user-defined rules**, and uses **AI-based rule generation** to improve filtering.  

## 🔥 Features  

👉 **Gmail API Integration** – Fetches emails directly from Gmail.  
👉 **Rule-Based Email Filtering** – Moves emails, flags, marks as read/unread, etc.  
👉 **AI-Powered Rule Learning** – Automatically generates rules based on user behavior.  
👉 **Automated Scheduling** – Runs rules periodically in the background.  
👉 **Logging & Debugging** – Tracks applied rules and user actions for transparency.  

---

## 🛠️ **Tech Stack**  
🔹 **Python** – Core scripting language  
🔹 **PostgreSQL** – Stores fetched emails  
🔹 **Gmail API** – Fetches emails securely  
🔹 **spaCy & NLP** – AI rule generation  
🔹 **BeautifulSoup** – HTML email parsing  
🔹 **APScheduler** – Automates rule execution  

---

## 👤 **Folder Structure**  
```
📆 gmail-rule-processor  
 └📂 config                # Configuration files (rules, credentials, logs)  
   ├📄 rules.json         # User-defined & AI-generated rules  
   ├📄 user_actions.json  # Logs of user actions  
   ├📄 credentials.json   # Gmail API credentials  
 └📂 database              # Database connection  
   ├📄 db_connection.py   # PostgreSQL connection setup  
 └📂 queries               # SQL queries for rule execution  
   ├📄 emailqueries.py    # SQL queries for filtering & updating emails  
 └📂 scripts               # Core functionality  
   ├📄 fetch_emails.py    # Fetches emails from Gmail  
   ├📄 process_emails.py  # Applies rules to fetched emails  
   ├📄 ai_rule_generator.py  # AI-based rule learning  
   ├📄 scheduler.py       # Background task scheduler  
 ├📄 .gitignore           # Ignore sensitive files (logs, credentials)  
 ├📄 README.md            # This file  
 ├📄 requirements.txt      # Python dependencies  
```

---

## 🚀 **Installation & Setup**  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Jayakanth2005/gmail_automation  
cd gmail-rule-processor
```

### 2️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Gmail API Credentials  
- Go to [Google Cloud Console](https://console.cloud.google.com/)  
- Enable **Gmail API**  
- Download `credentials.json` and place it inside `config/`  

### 4️⃣ Configure PostgreSQL Database  
- Update `database/db_connection.py` with your **database credentials**.  
- Create the `emails` table:  
```sql
CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    message_id TEXT UNIQUE,
    from_email TEXT,
    to_email TEXT,
    subject TEXT,
    message_body TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    label TEXT DEFAULT 'Inbox'
);
```

---

📌 **Usage Guide**  

1️⃣ Fetch Emails from Gmail**  
```bash
python scripts/fetch_emails.py
```
📌 **What it does:** Connects to Gmail API and stores emails in the database.

**2️⃣ Apply User & AI Rules**  
```bash
python scripts/process_emails.py
```
📌 **What it does:** Reads `rules.json` and applies actions like moving, flagging, or deleting emails.

 **3️⃣ Generate AI-Based Rules**  
```bash
python scripts/ai_rule_generator.py
```
📌 **What it does:** Learns from `user_actions.json` and automatically suggests new filtering rules.

 **4️⃣ Enable Auto-Scheduling**  
```bash
python scripts/scheduler.py
```
📌 **What it does:** Runs email processing **every 1 hour** in the background.

---

 ✨ **How Rules Work (Example in `rules.json`)**  
```json
{
    "field": "subject",
    "predicate": "Contains",
    "value": "Invoice",
    "action": "Move to Folder: Finance"
}
```
📌 **This moves all emails with "Invoice" in the subject to the "Finance" folder.**  

---

🚀 **Future Enhancements**  
👉 **AI Rule Optimization** – Improve accuracy using machine learning.  
👉 **Multi-User Support** – Allow different rules for different users.  
👉 **Web Dashboard** – GUI to create and manage email rules easily.  

---

💪 **Contributing**  
1. Fork the repo & create a new branch (`feature-xyz`).  
2. Make changes and test thoroughly.  
3. Submit a **pull request** with details.  

---

📚 **License**  
This project is licensed under the **MIT License**. See `LICENSE` for details.

---

 ✨ **Author & Credits**  
👤 **Your Name**  
📧 your.email@example.com  
🔗 [LinkedIn](https://linkedin.com/in/yourname) | [GitHub](https://github.com/yourusername)  

---

📌 **If you found this project useful, consider giving it a ⭐ on GitHub!** 🚀✨

