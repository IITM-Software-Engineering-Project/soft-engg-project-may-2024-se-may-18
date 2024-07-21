from fastapi import APIRouter, HTTPException, Request, FastAPI

root_router = APIRouter()


@root_router.get("/")
async def read_root():
    return {"message": "Hello World from Seek Next!"}
