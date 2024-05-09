"""from fastapi import HTTPException, FastAPI
import pyodbc
import uvicorn

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-IOILHI2;DATABASE=FaceCriminalDetection' ';Trusted_Connection=yes;')

app = FastAPI()


def check_user_details(email, password):
    query = "SELECT * FROM users WHERE username = " + str(email) + "and password = " + str(password)
    cursor = conn.cursor()
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result


def authenticate_user(input_email: str, input_password: str):
    cursor = conn.cursor()
    cursor.execute("SELECT *  FROM dbo.users WHERE email = ?", (input_email,))
    user = cursor.fetchone()
    if user.password == input_password and user.email == input_email:
        return "user"
    else:
        return "INVALID EMAIL OR PASSWORD"


@app.post("/login")
async def login(email: str, password: str):
    check_user_details(email, password)


if "__name__" == "__main__":
    uvicorn.run(app, port=8000, host="127.0.0.1")
"""

import pyodbc
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# Define your SQL Server connection string
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-IOILHI2;DATABASE=FaceCriminalDetection' ';Trusted_Connection=yes;')


# Function to connect to SQL Server
def connect_to_sql_server():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        return conn, cursor
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")
        return None, None


# Function to authenticate user
def authenticate_user(email: str, password: str):
    conn, cursor = connect_to_sql_server()
    if conn and cursor:
        try:
            query = f"SELECT * FROM users WHERE email='{email}' AND password='{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            if user:
                return {"email": email,
                        "name": user.name}  # Assuming your users table has columns 'email' and 'name'
            else:
                return None
        except pyodbc.Error as e:
            print(f"Error executing SQL query: {e}")
            return None
        finally:
            conn.close()


# Define request body model
class UserLogin(BaseModel):
    email: str
    password: str


@app.get("/")
async def root():
    return {"message": "Hello, Flutter!"}


users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]


# Define a route to retrieve users
@app.get("/users")
async def get_users():
    return {"users": users}


# Define login endpoint
@app.post("/login")
async def login(email: str, password: str):
    user = UserLogin(email=email, password=password)
    auth_user = authenticate_user(user.email, user.password)
    if auth_user:
        return {f"message": "Login successful ", **auth_user}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
