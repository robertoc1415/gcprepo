import sys
# from sqlalchemy import create_engine
from fastapi import FastAPI, HTTPException

import sqlite3

app = FastAPI()

# Establecer conexión con la base de datos
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Crear tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username text)''')


@app.post("/usernames10000")
async def add_username(username: str):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        raise HTTPException(status_code=400, detail="Username already exists")

    # Agregar usuario
    c.execute("INSERT INTO users (username) VALUES (?)", (username,))

    # Guardar cambios
    conn.commit()

    return {"username": username}


@app.get("/usernames20")
async def read_usernames():
    c.execute("SELECT * FROM users")
    usernames = [row[0] for row in c.fetchall()]
    return {"usernames": usernames}

# Cerrar conexión al finalizar


@app.on_event("shutdown")
def close_db_connection():
    conn.close()