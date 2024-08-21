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
    # Parse JSON body
    data = await request.json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    # Validate input fields
    if not username or not email or not password or not role:
        raise HTTPException(
            status_code=400, detail="All fields (username, email, password, role) are required")

    # Check if user already exists by username or email
    existing_user = session.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user instance
    new_user = User(
        username=username,
        email=email,
        password=hashed_password.decode('utf-8'),
        role=role,
        last_login=datetime.now()  # Or None, depending on your design
    )

    # Add the new user to the database
    session.add(new_user)
    session.commit()

    return {"message": "User registered successfully"}


@auth_router.post("/sign-in",
                  description="Login to the application",
                  response_description="Access Token and Token Type",
                  tags=["authentication"],
                  )
async def login(request: Request, session: Session = Depends(get_db)):
    # Parse JSON body
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    # Check if both username and password are provided
    if not username or not password:
        raise HTTPException(
            status_code=400, detail="Username and password are required")

    # Fetch user from the database
    user = session.query(User).filter(User.username == username).first()

    # Check if the user exists
    if not user:
        raise HTTPException(
            status_code=400, detail="User is not registered")

    # Verify the password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    # Update the last login time
    user.last_login = datetime.now()

    # User data for the token
    user_id = user.id
    username = user.username
    role = user.role
    email = user.email

    # Save the updated user data
    session.add(user)
    session.commit()

    # Create JWT access token
    access_token_expires = timedelta(minutes=45)
    access_token = jwt.encode(
        {"username": username, "exp": datetime.now() + access_token_expires,
         "role": role, "email": email},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # Return token and user information
    return {
        "access_token": access_token,
        "id": user_id,
        "role": role,
        "email": email,
        "username": username,
        "detail": "Login successful"
    }


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
            user_id = user.id
            username = user.username
            role = user.role
            email = user.email

            return {"id": user_id, "role": role, "email": email, "username": username}

        return {"username": username, "role": role, "email": email}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
