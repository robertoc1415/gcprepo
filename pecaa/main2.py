# import sys

# from fastapi import FastAPI, HTTPException

# # version = f"{sys.version_info.major}.{sys.version_info.minor}"

# # app = FastAPI()


# # @app.get("/")
# # async def read_root():
# #     message = f"Hello world! Mother fukerss {version}"
# #     return {"message": message}

# # usernames = []

# # @app.post("/usernames")
# # async def add_username(username: str):
# #     if username in usernames:
# #         raise HTTPException(status_code=400, detail="Username already exists")
# #     usernames.append(username)
# #     return {"username": username}

# # @app.get("/usernames")
# # async def read_usernames():
# #     return {"usernames": usernames}

# import sqlite3

# app = FastAPI()

# # Establecer conexión con la base de datos
# conn = sqlite3.connect('users.db')
# c = conn.cursor()

# # Crear tabla si no existe
# c.execute('''CREATE TABLE IF NOT EXISTS users
#              (username text)''')


# @app.post("/usernames")
# async def add_username(username: str):
#     c.execute("SELECT * FROM users WHERE username=?", (username,))
#     if c.fetchone():
#         raise HTTPException(status_code=400, detail="Username already exists")

#     # Agregar usuario
#     c.execute("INSERT INTO users (username) VALUES (?)", (username,))

#     # Guardar cambios
#     conn.commit()

#     return {"username": username}

# @app.get("/usernames")
# async def read_usernames():
#     c.execute("SELECT * FROM users")
#     usernames = [row[0] for row in c.fetchall()]
#     return {"usernames": usernames}

# @app.delete("/usernames/{username}")
# async def delete_username(username: str):
#     c.execute("SELECT * FROM users WHERE username=?", (username,))
#     if not c.fetchone():
#         raise HTTPException(status_code=404, detail="Username not found")

#     # Eliminar usuario
#     c.execute("DELETE FROM users WHERE username=?", (username,))

#     # Guardar cambios
#     conn.commit()

#     return {"username": username}

# @app.put("/usernames/{username}")
# async def update_username(username: str, new_username: str):
#     c.execute("SELECT * FROM users WHERE username=?", (username,))
#     if not c.fetchone():
#         raise HTTPException(status_code=404, detail="Username not found")

#     c.execute("SELECT * FROM users WHERE username=?", (new_username,))
#     if c.fetchone():
#         raise HTTPException(status_code=400, detail="New username already exists")

#     # Actualizar usuario
#     c.execute("UPDATE users SET username=? WHERE username=?", (new_username, username))

#     # Guardar cambios
#     conn.commit()

#     return {"username": new_username}



# # Cerrar conexión al finalizar
# @app.on_event("shutdown")
# def close_db_connection():
#     conn.close()


import sys
# from sqlalchemy import create_engine
from fastapi import FastAPI, HTTPException

# version = f"{sys.version_info.major}.{sys.version_info.minor}"

# app = FastAPI()


# @app.get("/")
# async def read_root():
#     message = f"Hello world! Mother fukerss {version}"
#     return {"message": message}

# usernames = []

# @app.post("/usernames")
# async def add_username(username: str):
#     if username in usernames:
#         raise HTTPException(status_code=400, detail="Username already exists")
#     usernames.append(username)
#     return {"username": username}

# @app.get("/usernames")
# async def read_usernames():
#     return {"usernames": usernames}


# import json
# with open("config.json") as f:
#     data = json.load(f)
#     conn_str = f"mssql+pyodbc://{data['user']}:{data['password']}@{data['server']}/{data['database']}?driver=ODBC+Driver+17+for+SQL+Server"

# connection_string = 'mssql+pyodbc://{0}:{1}@{2}/{3}?driver=ODBC+Driver+17+for+SQL+Server'.format(
#     "roberto.isajar", "your_password", "apicrud.database.windows.net", "your_db_name")
# engine = create_engine(connection_string)
# connection = engine.connect()
import pyodbc

server = 'apicrud.database.windows.net' 
database = 'apidatabase' 
username = 'roberto.isajar' 
password = 'Fkf63dLay12c!' 
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

def check_connection():
    if conn:
        print("Connection successful.")
    else:
        print("Connection failed.")

check_connection()

app = FastAPI()

# Establecer conexión con la base de datos
c = conn.cursor()

# Crear tabla si no existe
# c.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(255), age INT)")
# conn.commit()


@app.post("/users/{user_id}")
def create_user(user_id: int, name: str, age: int):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (id, name, age) VALUES ({user_id}, '{name}', {age})")
    conn.commit()
    return {"message": "User created successfully"}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    user = cursor.fetchone()
    if user:
        return {"id": user[0], "name": user[1], "age": user[2]}
    else:
        return {"message": "User not found"}


@app.get("/users/name/{user_name}")
def read_user_by_name(user_name: str):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE name='{user_name}'")
    user = cursor.fetchone()
    if user:
        return {"id": user[0], "name": user[1], "age": user[2]}
    else:
        return {"message": "User not found"}


# @app.put("/usernames")
# async def add_username(username: str):
#     c.execute("SELECT * FROM users WHERE username=?", (username,))
#     if c.fetchone():
#         raise HTTPException(status_code=400, detail="Username already exists")

#     # Agregar usuario
#     c.execute("INSERT INTO users (username) VALUES (?)", (username,))

#     # Guardar cambios
#     conn.commit()

#     return {"username": username}

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, age: int):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    if cursor.fetchone():
        cursor.execute(f"UPDATE users SET name='{name}', age={age} WHERE id={user_id}")
        conn.commit()
        return {"message": "User updated successfully"}
    else:
        return {"message": "Error updating user: User not found"}


    
@app.get("/usernames")
async def read_usernames():
    c.execute("SELECT * FROM users")
    usernames = [row[0] for row in c.fetchall()]
    return {"usernames": usernames}

# Cerrar conexión al finalizar


@app.on_event("shutdown")
def close_db_connection():
    conn.close()