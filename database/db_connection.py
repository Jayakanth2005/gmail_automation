import psycopg2

# PostgreSQL Configuration 
DB_CONFIG = {
    "dbname": "gmail_db",   # Replace with your actual database name
    "user": "postgres",           # Replace with your database user
    "password": "jayakanth",   # Replace with your database password
    "host": "localhost",              
    "port": "5432"                    # Default PostgreSQL port
}

def get_db_connection():
    """Establish and return a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Database connection successful!")
        return conn
    except psycopg2.Error as e:
        print("❌ Error connecting to database:", e)
        return None

def create_tables():
    """Create emails and rules tables if they do not exist."""
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor()

    # Create Emails Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id SERIAL PRIMARY KEY,
        message_id VARCHAR(100) UNIQUE,
        from_email VARCHAR(100) NOT NULL,
        to_email VARCHAR(255) NOT NULL,
        subject VARCHAR(255) NOT NULL,
        message_body TEXT,
        received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_read BOOLEAN DEFAULT FALSE,
        is_important BOOLEAN DEFAULT FALSE,
        is_flagged BOOLEAN DEFAULT FALSE,    
        label TEXT
    );
    """)

    # Create Rules Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rules (
        id SERIAL PRIMARY KEY,
        field TEXT CHECK (field IN ('From', 'To', 'Subject', 'Message', 'Received Date/Time')) NOT NULL,
        predicate TEXT CHECK (predicate IN ('Contains', 'Does not contain', 'Equals', 'Does not equal', 'Less than', 'Greater than')) NOT NULL,
        value TEXT NOT NULL,
        rule_predicate TEXT CHECK (rule_predicate IN ('All', 'Any')) NOT NULL,
        action TEXT CHECK (action IN ('Mark as read', 'Mark as unread', 'Move Message')) NOT NULL
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables created successfully (if not already present).")

# Run the script to create tables when executed
if __name__ == "__main__":
    create_tables()
