import json
import os
import spacy
import pandas as pd

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_PATH = os.path.join(BASE_DIR, "config", "user_actions.json")
RULES_PATH = os.path.join(BASE_DIR, "config", "rules.json")


def extract_keywords(text):
    """Extract important keywords from the email subject/body."""
    doc = nlp(text)
    keywords = [token.lemma_ for token in doc if token.pos_ in ("NOUN", "PROPN")]
    return keywords

#If the user actions are done for atleast 3 times then log is added as a rule
def generate_rules():
    """Analyze user behavior and generate AI-based rules."""
    if not os.path.exists(LOGS_PATH):
        print("No user logs found.")
        return

    # Load user logs
    with open(LOGS_PATH, "r") as f:
        logs = json.load(f)

    df = pd.DataFrame(logs)

    if df.empty:
        print("No actions found in logs.")
        return

    # Group by field & action to find patterns
    grouped = df.groupby(["field", "value", "action"]).size().reset_index(name="count")

    new_rules = []
    for _, row in grouped.iterrows():
        field, value, action, count = row["field"], row["value"], row["action"], row["count"]

        # Generate rules if an action occurs frequently
        if count >= 3:  # If the same action happens 3+ times, suggest a rule
            rule = {
                "field": field.replace('"', ""),  # Remove quotes
                "predicate": "Contains",
                "value": value,
                "action": action
            }
            new_rules.append(rule)

    # Save new rules to `rules.json`
    if new_rules:
        with open(RULES_PATH, "r") as f:
            existing_rules = json.load(f)

        existing_rules.extend(new_rules)

        with open(RULES_PATH, "w") as f:
            json.dump(existing_rules, f, indent=4)

        print("✅ AI-based rules added to rules.json")
    else:
        print("No new rules generated.")


if __name__ == "__main__":
    generate_rules()
