
from fastapi import Form, APIRouter, HTTPException, Body
from typing import Annotated

router = APIRouter(prefix="/support", tags=["Support"])

# Path operation decorator for the support endpoint that accepts form data
@router.post("/support")
async def support_endpoint(title: Annotated[str, Form()], message: Annotated[str, Form()]):
    return {"title": title, "message": message}