"""
Script to create the PostgreSQL database.
Run this before recreate_db.py
"""
import psycopg2
from psycopg2 import sql

def create_database():
    try:
        # Connect to PostgreSQL server (default postgres database)
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="vikas123",
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'swiftride_db'")
        exists = cursor.fetchone()
        
        if exists:
            print("Database 'swiftride_db' already exists!")
        else:
            # Create database
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier('swiftride_db')
            ))
            print("Database 'swiftride_db' created successfully!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error: {e}")
        print("\nMake sure PostgreSQL is running and the password is correct.")

if __name__ == "__main__":
    create_database()
