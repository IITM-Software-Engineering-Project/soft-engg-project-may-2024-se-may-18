from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from resources.test import root_router
from database.db import init_db
import uvicorn


app = FastAPI()
init_db()

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

if __name__ == "__main__":
    uvicorn.run(app, port=8000, debug=True)
