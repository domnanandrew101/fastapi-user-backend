from fastapi import FastAPI
import sqlite3

from passlib.context import CryptContext
pwd_context = CryptContext(schemes =['bcrypt'], deprecated = 'auto')

from dotenv import load_dotenv
import os

load_dotenv()

secret = os.getenv('SECRET_KEY')

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

app = FastAPI()

@app.get('/')
def home():
    return{'message':'Server is running'}

@app.get('/users')
def get_users():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()
    conn.close()
    return all_users

from pydantic import BaseModel

class User(BaseModel):
    name:str
    email:str
    age:int
    password:str

@app.post('/users')
def create_user(user:User):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    hashed_pw = hash_password(user.password)
    cursor.execute('INSERT INTO users (name, email, age, password) VALUES(?, ?, ?, ?)',
    (user.name, user.email, user.age, hashed_pw))
    conn.commit()
    conn.close()
    return{'message':'User created successfully'}

@app.post('/login')
def login(email: str, password: str):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
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
def get_user(email:str):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    conn.close()
    return result

@app.put('/users/{email}')
def update_user(email:str, user:User):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name = ?, email = ?, age = ? WHERE email = ?',
    (user.name, user.email, user.age, email))
    conn.commit()
    conn.close()
    return{'message': 'User updated successfully'}

@app.delete('/users/{email}')
def delete_user(email:str):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE email = ?', (email,))
    conn.commit()
    conn.close()
    return{'message': 'User deleted successfully'}

