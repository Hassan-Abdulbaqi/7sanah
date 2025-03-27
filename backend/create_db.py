#!/usr/bin/env python
"""
Script to create a PostgreSQL database for the Quran Khatmah application.
This should be run only once when setting up the production environment.
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print("Error: .env file not found. Please create one based on .env.example")
    sys.exit(1)

# Get database connection parameters from environment variables
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

if not all([db_host, db_port, db_user, db_password, db_name]):
    print("Error: Missing database configuration in .env file")
    sys.exit(1)

# Connect to the default 'postgres' database to create our app database
conn = None
try:
    # Connect to default database
    print(f"Connecting to PostgreSQL server at {db_host}:{db_port}...")
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        dbname="postgres"  # Connect to the default postgres database
    )
    conn.autocommit = True  # Needed for database creation
    cursor = conn.cursor()
    
    # Check if database already exists
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()
    
    if exists:
        print(f"Database '{db_name}' already exists.")
    else:
        # Create the database
        print(f"Creating database '{db_name}'...")
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully!")
    
    cursor.close()
    
    # Now connect to our newly created database to verify it works
    print(f"Connecting to '{db_name}' database to verify it's working...")
    app_conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        dbname=db_name
    )
    app_conn.close()
    print("Database connection verified successfully!")
    
    print("\nNext steps:")
    print("1. Run 'python manage.py migrate' to create database tables")
    print("2. Run 'python manage.py createsuperuser' to create an admin user")
    print("3. Run 'python manage.py collectstatic' to collect static files")
    
except psycopg2.Error as e:
    print(f"Error: {e}")
    sys.exit(1)
finally:
    if conn:
        conn.close() 