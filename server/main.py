from fastapi import Depends, FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from resources.test import root_router
from resources.auth import auth_router
from resources.gen_ai import genai_router
from resources.student import student_router
from resources.instructor import instructor_router
from resources.admin import admin_router
from resources.code_computing import code_router
from resources.code_runner import code_runner_router
import uvicorn
from api.middleware.verify_token import TokenAuthMiddleware

app = FastAPI(middleware=[Middleware(TokenAuthMiddleware)])

# List of origins that should be allowed to make cross-origin requests
origins = [
    "http://localhost:5173",  # Frontend running on localhost:5173
    "http://your-frontend-domain.com"  # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Or specify allowed methods like ["GET", "POST"]
    allow_headers=["*"],  # Or specify allowed headers
)

app.include_router(root_router)
app.include_router(auth_router)
app.include_router(genai_router)
app.include_router(instructor_router)
app.include_router(code_router)
app.include_router(student_router)
app.include_router(admin_router)
app.include_router(code_runner_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, debug=True)
