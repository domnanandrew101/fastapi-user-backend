import psycopg2
import os
from dotenv import load_dotenv

# Load the environment variables from your .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def setup_database():
    try:
        # Connect to Render
        print("Connecting to Render PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Postgres syntax for creating the table
        # We use SERIAL for an auto-incrementing ID, and make email UNIQUE
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            age INTEGER NOT NULL,
            password TEXT NOT NULL
        );
        """
        
        cursor.execute(create_table_query)
        conn.commit()
        print("Success! The 'users' table has been created on Render.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()