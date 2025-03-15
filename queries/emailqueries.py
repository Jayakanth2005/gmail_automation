
# Query to retrieve emails based on different predicates
EMAIL_QUERIES = {
    "Contains": "SELECT * FROM emails WHERE {field} ILIKE %s",
    "Equals": "SELECT * FROM emails WHERE {field} = %s",
    "Starts With": "SELECT * FROM emails WHERE {field} ILIKE %s",
    "Ends With": "SELECT * FROM emails WHERE {field} ILIKE %s",
    "Exists": "SELECT * FROM emails WHERE {field} IS NOT NULL"
}

# Query to update email based on actions
EMAIL_ACTIONS = {
    "Mark as Unread": "UPDATE emails SET is_read = FALSE WHERE id = %s",
    "Mark as Important": "UPDATE emails SET is_important = TRUE WHERE id = %s",
    "Flag": "UPDATE emails SET is_flagged = TRUE WHERE id = %s",
    "Move to Junk": "UPDATE emails SET label = 'Junk' WHERE id = %s",
    "Move to Spam": "UPDATE emails SET label = 'Spam' WHERE id = %s",
    "Mark as Read": "UPDATE emails SET is_read = TRUE WHERE id = %s",
    "Move to Folder": "UPDATE emails SET label = %s WHERE id = %s"
}
