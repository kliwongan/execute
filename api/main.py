import os, sys
import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Machinery to help out with relative import errors
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from exec import check_unsafe_code, exec_code_secure
from persist import persist

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeUpload(BaseModel):
    code: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/test_code")
async def test_code(params: CodeUpload):
    params = params.dict()
    code = params["code"]
    output = ""
    if check_unsafe_code(code):
        raise HTTPException(
            status_code=400,
            detail="Code was unsafe!",
            headers={"X-Error": "Unsafe code posted"},
        )

    output = exec_code_secure(code)
    return {"output": output}


@app.post("/submit_code")
async def test_code(params: CodeUpload):
    params = params.dict()
    code = params["code"]
    output = ""
    if check_unsafe_code(code):
        raise HTTPException(
            status_code=400,
            detail="Code was unsafe!",
            headers={"X-Error": "Unsafe code posted"},
        )

    output = exec_code_secure(code)
    try:
        persist_code(code, output)
    except e:
        raise HTTPException(
            status_code=400,
            detail="Saving to database failed!",
            headers={"X-Error": "Saving to database failed"},
        )
    return {"output": output}
