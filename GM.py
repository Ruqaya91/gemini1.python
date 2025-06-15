import mysql.connector
from mysql.connector import Error

# --- Database Configuration ---
# IMPORTANT: Replace these with your actual MySQL database credentials
DB_CONFIG = {
    'host': 'localhost',  # e.g., '127.0.0.1' or your database host
    'database': 'user_db', # The name of your database
    'user': 'your_user',   # Your MySQL username
    'password': 'your_password' # Your MySQL password
}

# --- Function to establish database connection ---
def create_db_connection():
    """
    Establishes a connection to the MySQL database.
    Returns the connection object if successful, None otherwise.
    """
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print(f"Successfully connected to MySQL database: {DB_CONFIG['database']}")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# --- Function to create users table (for demonstration) ---
def create_users_table(connection):
    """
    Creates a 'users' table if it doesn't exist.
    This function is for demonstration purposes to ensure the table is present.
    In a real application, you'd manage your schema through migrations.
    """
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)
        print("Table 'users' checked/created successfully.")
        connection.commit()
    except Error as e:
        print(f"Error creating/checking 'users' table: {e}")
    finally:
        cursor.close()

# --- Function to add a test user (for demonstration) ---
def add_test_user(connection, username, password):
    """
    Adds a test user to the 'users' table if they don't already exist.
    Password should ideally be hashed in a real application.
    """
    cursor = connection.cursor()
    try:
        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print(f"User '{username}' already exists. Skipping addition.")
            return

        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (username, password))
        connection.commit()
        print(f"Test user '{username}' added successfully.")
    except Error as e:
        print(f"Error adding test user: {e}")
    finally:
        cursor.close()

# --- Function to validate user credentials ---
def validate_credentials(connection, username, password):
    """
    Checks if the provided username and password are valid against the database.
    IMPORTANT: In a real application, passwords should be hashed (e.g., using bcrypt)
    and compared securely, not stored/compared in plain text as shown here.
    """
    if not connection:
        print("No database connection available.")
        return False

    cursor = connection.cursor()
    try:
        # Using parameterized query to prevent SQL injection
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        result = cursor.fetchone() # Fetches the first matching row

        if result:
            print(f"\nAuthentication successful for user: {username}")
            return True
        else:
            print(f"\nAuthentication failed. Invalid username or password for: {username}")
            return False
    except Error as e:
        print(f"Error during credential validation: {e}")
        return False
    finally:
        cursor.close()

# --- Main execution block ---
if __name__ == "__main__":
    print("--- MySQL User Authentication Script ---")
    print("Prerequisites: ")
    print("1. Install mysql-connector-python: pip install mysql-connector-python")
    print("2. Ensure MySQL server is running.")
    print("3. Create a database named 'user_db' (or adjust DB_CONFIG).")
    print("4. Grant necessary permissions to 'your_user' (or adjust DB_CONFIG).")
    print("-" * 35)

    db_connection = None
    try:
        db_connection = create_db_connection()

        if db_connection:
            # For demonstration: Ensure table exists and add a test user
            create_users_table(db_connection)
            add_test_user(db_connection, "testuser", "testpass")
            add_test_user(db_connection, "admin", "admin123")

            while True:
                print("\nEnter your credentials to log in (type 'exit' to quit):")
                input_username = input("Username: ")
                if input_username.lower() == 'exit':
                    break
                input_password = input("Password: ")

                validate_credentials(db_connection, input_username, input_password)
        else:
            print("Could not establish a database connection. Exiting.")

    finally:
        if db_connection and db_connection.is_connected():
            db_connection.close()
            print("\nMySQL connection closed.")
