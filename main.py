import uuid
from typing import List
import datetime
import pyrebase
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth, firestore

from model import SignUpSchema, LogInSchema, UpdateUserSchema, TaskCreateSchema, TaskUpdateSchema

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

app = FastAPI(docs_url="/")
db = firestore.client()

load_dotenv()

firebaseConfig = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTH_DOMAIN"),
    "projectId": os.getenv("PROJECT_ID"),
    "storageBucket": os.getenv("STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
    "appId": os.getenv("APP_ID"),
    "measurementId": os.getenv("MEASUREMENT_ID"),
    "databaseURL": os.getenv("DATABASE_URL")
}


def get_uid_from_token(authorization: str) -> str:
    try:
        token = authorization.split(" ")[1]
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.post('/signup')
async def signup(user_data: SignUpSchema):
    try:
        user = auth.create_user(
            email=user_data.email.strip(), password=user_data.password)
        db.collection("users").document(user.uid).set({
            "uid": user.uid,
            "email": user_data.email.strip(),
            "full_name": user_data.full_name.strip(),
            "created_at": datetime.datetime.utcnow()
        })
        return JSONResponse(content={"message": f"User account created for {user.uid}"}, status_code=201)
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already exists")

# login endpoint


@app.post("/login")
async def login(user_data: LogInSchema):
    try:
        firebase = pyrebase.initialize_app(firebaseConfig)
        auth_client = firebase.auth()
        user = auth_client.sign_in_with_email_and_password(
            user_data.email, user_data.password)
        return {
            "token": user.get("idToken"),

        }
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Credentials")


@app.get('/user/me')
async def get_profile(authorization: str = Header(...)):
    try:
        # Strip "Bearer " from header and verify
        token = authorization.split("Bearer ")[1]
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]

        user = auth.get_user(uid)
        return {
            "uid": uid,
            "email": user.email,
            "display_name": user.display_name,
            "created_at": user.user_metadata.creation_timestamp
        }
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Invalid or expired token: {e}")


@app.put('/user/update')
async def update_user(data: UpdateUserSchema, authorization: str = Header(...)):
    uid = get_uid_from_token(authorization)
    db.collection("users").document(uid).update(
        {"full_name": data.full_name.strip()})
    return {"message": "User updated successfully"}


@app.post("/tasks/")
async def create_task(task: TaskCreateSchema, authorization: str = Header(...)):

    uid = get_uid_from_token(authorization)

    task_id = str(uuid.uuid4())
    task_data = {
        "task_id": task_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow()
    }

    firebaseConfig = {
        "apiKey": "AIzaSyB_ZjIr10V2Cnyxv6konMYPF6GJNpKh7OA",
        "authDomain": "fir-auth-4a0e4.firebaseapp.com",
        "projectId": "fir-auth-4a0e4",
        "storageBucket": "fir-auth-4a0e4.firebasestorage.app",
        "messagingSenderId": "1057990124939",
        "appId": "1:1057990124939:web:6d8634b4766b771378fb8e",
        "measurementId": "G-49343NKSJS",
        "databaseURL": ""
    }

    db.collection("tasks").document(uid).collection(
        "user_tasks").document(task_id).set(task_data)

    return {"message": "Task created", "task_id": task_id}


@app.get("/tasks/")
async def get_tasks(authorization: str = Header(...)):
    uid = get_uid_from_token(authorization)
    print("GET UID:", uid)
    tasks_ref = db.collection("tasks").document(
        uid).collection("user_tasks").stream()
    tasks = [task.to_dict() for task in tasks_ref]
    return tasks


@app.get("/tasks/{task_id}")
async def get_task(task_id: str, authorization: str = Header(...)):
    uid = get_uid_from_token(authorization)
    doc = db.collection("tasks").document(uid).collection(
        "user_tasks").document(task_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Task not found")
    return doc.to_dict()


@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: TaskUpdateSchema, authorization: str = Header(...)):
    uid = get_uid_from_token(authorization)
    task_ref = db.collection("tasks").document(
        uid).collection("user_tasks").document(task_id)
    if not task_ref.get().exists:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = {k: v for k, v in task.dict().items() if v is not None}
    update_data["updated_at"] = datetime.datetime.utcnow()
    task_ref.update(update_data)
    return {"message": "Task updated"}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str, authorization: str = Header(...)):
    uid = get_uid_from_token(authorization)
    task_ref = db.collection("tasks").document(
        uid).collection("user_tasks").document(task_id)
    if not task_ref.get().exists:
        raise HTTPException(status_code=404, detail="Task not found")
    task_ref.delete()
    return {"message": "Task deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
