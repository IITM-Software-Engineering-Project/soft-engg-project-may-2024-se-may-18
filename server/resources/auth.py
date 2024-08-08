from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, Request, Depends
from database.models import User, session
from datetime import datetime, timedelta
import bcrypt
import jwt
from database.db_sql import init_db
from sqlalchemy.orm import sessionmaker, Session
auth_router = APIRouter()

SECRET_KEY = 'secret-key'
ALGORITHM = "HS256"
def get_db():
    engine = init_db()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/register",
                  description="Register a new user to the portal",
                  response_description="Message indicating success or failure",
                  tags=["authentication"],
                  )
async def register(request: Request, session: Session = Depends(get_db)):
    data = await request.json()
    username = data["username"]
    email = data["email"]
    password = data["password"]
    role = data["role"]

    # Check if user is already registered
    user = session.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(username=username, email=email,
                    password=hashed_password.decode('utf-8'), role=role, last_login=None)
    try:
        session.add(new_user)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Error registering user")

    return {"message": "User registered successfully"}


@auth_router.post("/login",
                  description="Login to the application",
                  response_description="Access Token and Token Type",
                  tags=["authentication"],
                  )
async def login(request: Request, session: Session = Depends(get_db)):
    data = await request.json()
    username = data["username"]
    password = data["password"]

    user = session.query(User).filter(User.username == username).first()
    

    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    # Verify the password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    user.last_login = datetime.now()

    session.add(user)
    session.commit()


    access_token_expires = timedelta(minutes=45)
    access_token = jwt.encode(
        {"sub": username, "exp": datetime.now() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}
