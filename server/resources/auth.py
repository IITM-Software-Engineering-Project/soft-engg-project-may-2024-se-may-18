from fastapi import APIRouter, HTTPException, Request, Depends
from database.models import User, session
from datetime import datetime, timedelta
import bcrypt
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.exc import IntegrityError

auth_router = APIRouter()

SECRET_KEY = 'secret-key'
ALGORITHM = "HS256"

security = HTTPBearer()


@auth_router.post("/register",
                  description="Register a new user to the portal",
                  response_description="Message indicating success or failure",
                  tags=["authentication"],
                  )
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
                    password=hashed_password.decode('utf-8'), role=role,
                    last_login=datetime.now()
                    )

    try:
        with session.begin() as db:
            db.add(new_user)
            db.commit()
            db.close()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Error registering user")

    return {"message": "User registered successfully"}


@auth_router.post("/login",
                  description="Login to the application",
                  response_description="Access Token and Token Type",
                  tags=["authentication"],
                  )
async def login(request: Request):
    data = await request.json()
    username = data["username"]
    password = data["password"]

    with session.begin() as db:
        user = db.query(User).filter(User.username == username).first()
        db.close()

    if not user:
        raise HTTPException(
            status_code=400, detail="User does not exist")

    # Verify the password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    user.last_login = datetime.now()

    username = user.username
    role = user.role
    email = user.email

    with session.begin() as db:
        db.add(user)
        db.commit()
        db.close()

    access_token_expires = timedelta(minutes=45)
    access_token = jwt.encode(
        {"username": username, "exp": datetime.now() + access_token_expires,
         "role": role, "email": email},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "role": role, "email": email, username: username}


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
