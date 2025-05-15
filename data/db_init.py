import sqlite3

def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('aidence.db')
    cursor = conn.cursor()

    # SQL statements to create tables
    sql_statements = [
        """CREATE TABLE IF NOT EXISTS User (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            type INTEGER,
            password TEXT,
            iban TEXT
        );""",
        """CREATE TABLE IF NOT EXISTS Session (
            sessionId TEXT PRIMARY KEY,
            userId INTEGER,
            expiryTime DATETIME,
            FOREIGN KEY (userId) REFERENCES User(userId)
        );""",
        """CREATE TABLE IF NOT EXISTS CtScan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image BLOB,
            createdAt DATETIME,
            owner INTEGER,
            FOREIGN KEY (owner) REFERENCES User(userId)
        );""",
        """CREATE TABLE IF NOT EXISTS CtScanAnalysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            createdAt DATETIME,
            score REAL,
            owner INTEGER,
            ctScan INTEGER,
            FOREIGN KEY (owner) REFERENCES User(userId),
            FOREIGN KEY (ctScan) REFERENCES CtScan(id)
        );""",
        """CREATE TABLE IF NOT EXISTS Report (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            createdAt DATETIME,
            ctScanAnalysis INTEGER,
            content TEXT,
            owner INTEGER,
            FOREIGN KEY (owner) REFERENCES User(userId),
            FOREIGN KEY (ctScanAnalysis) REFERENCES CtScanAnalysis(id)
        );""",
        """CREATE TABLE IF NOT EXISTS Payment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            createdAt DATETIME,
            amount REAL,
            user INTEGER,
            FOREIGN KEY (user) REFERENCES User(userId)
        );""",

    ]

    # Execute each SQL statement
    for statement in sql_statements:
        cursor.execute(statement)

    # Insert a dummy user
    cursor.execute("""
        INSERT INTO User (username, email, type, password, iban)
        VALUES (?, ?, ?, ?, ?)
    """, ('dummy_user', 'dummy@example.com', 1, 'securepassword123', 'NL89370400440532013000'))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
