from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ssl
import os
from typing import Optional
from api.utils.openai_client import get_openai_response
from api.utils.file_handler import save_upload_file_temporarily

app = FastAPI(title="IITM Assignment API")
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import logging
logging.basicConfig(level=logging.INFO)

@app.post("/api/")
async def process_question(question: str = Form(...), file: Optional[UploadFile] = File(None)):
    logging.info(f"Received question: {question}")
    try:
        temp_file_path = None
        if file:
            temp_file_path = await save_upload_file_temporarily(file)
            logging.info(f"File saved to: {temp_file_path}")
        
        answer = await get_openai_response(question, temp_file_path)
        logging.info(f"Answer: {answer}")
        return {"answer": answer}
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
