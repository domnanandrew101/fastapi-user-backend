from fastapi import FastAPI
import psycopg2

from passlib.context import CryptContext
from dotenv import load_dotenv

import os
from pydantic import BaseModel

# --- Configuration & Auth Setup ---
load_dotenv()

secret = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# --- Database Helper ---
def get_db_connection():
    # Connects to your live Render database!
    return psycopg2.connect(DATABASE_URL)

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: int
    password: str

# --- Routes ---
@app.get('/')
def home():
    return {'message': 'Server is running'}

@app.get('/users')
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()
    conn.close()
    return all_users

@app.post('/users')
def create_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(user.password)
    # Notice the %s placeholders instead of ?
    cursor.execute('INSERT INTO users (name, email, age, password) VALUES(%s, %s, %s, %s)',
                   (user.name, user.email, user.age, hashed_pw))
    conn.commit()
    conn.close()
    return {'message': 'User created successfully'}

@app.post('/login')
def login(email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE email = %s', (email,))
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        return {'message': 'User not found'}

    stored_hash = result[0]

    if verify_password(password, stored_hash):
        return {'message': 'Login successful'}
    else:
        return {'message': 'Invalid password'}

@app.get('/users/{email}')
def get_user(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    result = cursor.fetchone()
    conn.close()
    return result

@app.put('/users/{email}')
def update_user(email: str, user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name = %s, email = %s, age = %s WHERE email = %s',
                   (user.name, user.email, user.age, email))
    conn.commit()
    conn.close()
    return {'message': 'User updated successfully'}

@app.delete('/users/{email}')
def delete_user(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE email = %s', (email,))
    conn.commit()
    conn.close()
    return {'message': 'User deleted successfully'}