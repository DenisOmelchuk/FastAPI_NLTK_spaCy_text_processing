from fastapi import FastAPI, HTTPException
from nltk_setup import download_nltk_data_packages
from contextlib import asynccontextmanager
from pydantic import BaseModel
import nltk

app = FastAPI()


class TextRequest(BaseModel):
    text: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    During the startup event, it ensures that all required NLTK packages are downloaded
    by calling the download_nltk_data_packages() function.
    """
    download_nltk_data_packages()
    yield


app.router.lifespan_context = lifespan


@app.post("/tokenize/")
async def tokenize_text(request: TextRequest):
    """
    Tokenizes the input text using NLTK's word_tokenize function.

    Args:
        request (TextRequest): Request body containing the text to tokenize.

    Returns:
        list: List of tokens extracted from the input text.

    Raises:
        HTTPException: If there is an error during tokenization or if input is not a string.
    """
    try:
        tokens = nltk.word_tokenize(request.text)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to tokenize text: {str(e)}")
