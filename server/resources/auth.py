from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, Request
from database.models import User, session
from datetime import datetime, timedelta
import bcrypt
import jwt

auth_router = APIRouter()

SECRET_KEY = 'secret-key'
ALGORITHM = "HS256"


@auth_router.post("/register")
async def register(request: Request):
    data = await request.json()
    username = data["username"]
    email = data["email"]
    password = data["password"]
    role = data["role"]

    # Check if user is already registered
    with session.begin() as db:
        user = db.query(User).filter(User.username == username).first()
        if user:
            raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(username=username, email=email,
                    password=hashed_password.decode('utf-8'), role=role, last_login=None)

    try:
        with session.begin() as db:
            db.add(new_user)
            db.commit()
            db.close()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Error registering user")

    return {"message": "User registered successfully"}


@auth_router.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data["username"]
    password = data["password"]

    with session.begin() as db:
        user = db.query(User).filter(User.username == username).first()
        db.close()

    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    # Verify the password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    user.last_login = datetime.now()

    with session.begin() as db:
        db.add(user)
        db.commit()
        db.close()

    access_token_expires = timedelta(minutes=45)
    access_token = jwt.encode(
        {"sub": username, "exp": datetime.now() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}
