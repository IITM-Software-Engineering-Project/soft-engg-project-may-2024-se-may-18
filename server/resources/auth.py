from fastapi import APIRouter, HTTPException, Request, Depends
from database.models import User, session
from datetime import datetime, timedelta
import bcrypt
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.exc import IntegrityError
from database.db_sql import init_db
from sqlalchemy.orm import sessionmaker, Session

auth_router = APIRouter()

SECRET_KEY = 'secret-key'
ALGORITHM = "HS256"

security = HTTPBearer()


def get_db():
    engine = init_db()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_router.post("/sign-up",
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
                    password=hashed_password.decode('utf-8'), role=role,
                    last_login=datetime.now()
                    )

    try:
        session.add(new_user)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Error registering user")

    return {"message": "User registered successfully"}


@auth_router.post("/sign-in",
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
            status_code=400, detail="User does not exist")

    # Verify the password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    user.last_login = datetime.now()

    user_id = user.id
    username = user.username
    role = user.role
    email = user.email

    session.add(user)
    session.commit()

    access_token_expires = timedelta(minutes=45)
    access_token = jwt.encode(
        {"username": username, "exp": datetime.now() + access_token_expires,
         "role": role, "email": email},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "id": user_id, "role": role, "email": email, "username": username}


@auth_router.get("/verify-token",
                 description="Verify JWT token",
                 response_description="User information if the token is valid",
                 tags=["authentication"],
                 )
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        role = payload.get("role")
        email = payload.get("email")

        # Optionally, you could verify the user exists in the database
        with session.begin() as db:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                raise HTTPException(
                    status_code=400, detail="User does not exist")

        return {"username": username, "role": role, "email": email}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
