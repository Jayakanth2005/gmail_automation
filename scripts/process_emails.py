import json
import os
import sys
import spacy
from apscheduler.schedulers.background import BackgroundScheduler
nlp = spacy.load("en_core_web_sm")


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_connection import get_db_connection
from queries.emailqueries import EMAIL_QUERIES, EMAIL_ACTIONS

# Get the absolute path of the project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(BASE_DIR, "config", "rules.json")  

LOGS_PATH = os.path.join(BASE_DIR, "config", "user_actions.json")  # New logs file


def log_user_action(email_id, field, value, action):
    """Log user actions for AI-based rule generation."""
    log_entry = {"email_id": email_id, "field": field, "value": value, "action": action}

    # Read existing logs
    if os.path.exists(LOGS_PATH):
        with open(LOGS_PATH, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    # Write updated logs
    with open(LOGS_PATH, "w") as f:
        json.dump(logs, f, indent=4)




def apply_rules():
    """Apply rule-based actions on emails stored in the database."""
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()

    # Load rules from JSON using the correct path
    with open(RULES_PATH, "r") as file:
        rules = json.load(file)

    for rule in rules:
        field = rule["field"].lower()  # Ensure lowercase column names
        predicate, value, action = rule["predicate"], rule["value"], rule["action"]

        # Map rule field names to actual database column names
        field_mapping = {
        "from": "from_email",       # Map 'From' → 'from_email'
        "to": "to_email",           # Map 'To' → 'to_email'
        "subject": "subject",       # Map 'Subject' → 'subject'
        "body": "message_body",     # Map 'Body' → 'message_body'
        "attachments": "label"      # Assuming 'folders' are stored under 'label' (change if incorrect)
    }
        
        field = field_mapping.get(field, field)  # Use mapped name if exists

        # Ensure the field is properly escaped
        field = f'"{field}"'  

        if predicate in EMAIL_QUERIES:
            query = EMAIL_QUERIES[predicate].format(field=field)

        if not value and predicate != "Exists":
            print(f"⚠️ Skipping rule with empty value: {rule}")
            continue

        # Construct queries based on predicate
        if predicate == "Contains":
            cursor.execute(query, (f"%{value}%",))
        elif predicate == "Equals":
            cursor.execute(query, (value,))
        elif predicate == "Starts With":
            cursor.execute(query, (f"{value}%",))
        elif predicate == "Ends With":
            cursor.execute(query, (f"%{value}",))
        elif predicate == "Exists":
            cursor.execute(query)
        else:
            continue  # Skip unsupported predicates


        matching_emails = cursor.fetchall()

        for email in matching_emails:
            email_id = email[0]

            log_user_action(email_id, field, value, action)
            if action in EMAIL_ACTIONS:
                    update_query = EMAIL_ACTIONS[action]
                    cursor.execute(update_query, (email_id,))
            elif action.startswith("Move to Folder:"):
                    folder_name = action.split(":")[1].strip()
                    cursor.execute(EMAIL_ACTIONS["Move to Folder"], (folder_name, email_id))

            print(f"✅ Applied rule: {rule} on email ID {email_id}")

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Rule-based email processing completed!")

scheduler = BackgroundScheduler()
scheduler.add_job(apply_rules, 'interval', hours=1)  # Run every 1 hour
scheduler.start()

if __name__ == "__main__":
    print("📅 Scheduled rule processing started... (Runs every 1 hour)")
    try:
        while True:
            pass  # Keeps the script running
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()



