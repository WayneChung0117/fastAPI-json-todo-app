# Example: Student System Management - Todo List API with FastAPI

from fastapi import FastAPI, status     # Creates the web app
                        # rovides standard HTTP status codes
from fastapi.responses import JSONResponse  # Enables custom status code + JSON return
from pydantic import BaseModel        # For validating input data with Pydantic
from typing import List, Optional      # For optional fields (used in updates)
from threading import Thread
from pyngrok import ngrok
import uvicorn
import random
import json
import os

#Allows Colab to expose local Flask server to public.
from pyngrok import ngrok, conf
conf.get_default().ngrok_path = "D:\\Wayne\\Learning\\Tool\\ngrok-v3\\ngrok.exe"

from dotenv import load_dotenv

# ✅ Load .env file
load_dotenv()

# ✅ Set your ngrok authtoken securely
ngrok_token = os.getenv("NGROK_AUTH_TOKEN")
ngrok.set_auth_token(ngrok_token)

# Kills any existing ngrok tunnels, avoiding conflicts when you re-run the cell.
ngrok.kill()

FILE_NAME  = "Students_test.json"

# Pydantic model for student
class Student(BaseModel):
    id: str
    name: str
    task: str
    status: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    task: Optional[str] = None
    status: Optional[str] = None
    
# Load and save functions
def load_students():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_students(students):
    with open(FILE_NAME, "w") as f:
        json.dump(students, f, indent=2)
        

# Create FastAPI instance
app = FastAPI()
PORT = random.randint(1025, 9999)

# Routes

# GET /
@app.get("/")
def index():
    return {"message": "✅ Student Management from FastAPI - V1.2"}

# GET /students
@app.get("/students")
def get_students():
    return load_students()

# POST /students
@app.post("/students", status_code=status.HTTP_201_CREATED)
def add_student(student: Student):
    students = load_students()
    students.append(student.dict())
    save_students(students)
    return {"message": "✅ Student added", "student": student}

# PUT /students/{id}
@app.put("/students/{id}")
def update_status(id: str, updated_data: StudentUpdate):
    students = load_students()

    for s in students:
        if s["id"] == id:
          update_dict = updated_data.dict(exclude_unset=True)  # 只取得實際傳入的欄位
          for key in update_dict:
              s[key] = update_dict[key]

          save_students(students)
          return {"message": "✅ Student updated", "student": s}

    return JSONResponse(status_code=404, content={"error": "❌ Student not found"})

# DELETE /students/{id}
@app.delete("/students/{id}")
def delete_student(id: str):
    students = load_students()
    new_students = [s for s in students if s["id"] != id]

    if len(new_students) == len(students):
        return JSONResponse(status_code=404, content={"error": "❌ Student not found"})

    save_students(new_students)
    return {"message": "✅ Student deleted", "students": new_students}

# Run the app
def run():
    uvicorn.run(app, port=PORT)

# Kill old tunnels
ngrok.kill()

# Start the server in background
Thread(target=run).start()

# Start ngrok tunnel
public_url = ngrok.connect(PORT)
print("🌐 Public URL:", public_url)