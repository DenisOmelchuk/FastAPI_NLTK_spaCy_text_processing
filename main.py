from fastapi import FastAPI, HTTPException, Request
from nltk_setup import download_nltk_data_packages
from contextlib import asynccontextmanager
from pydantic import BaseModel
import nltk
import spacy
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins / You could change it to your web-page domain
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)


# Security headers middleware setup
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"

    """
    Set Content-Security-Policy to restrict all content sources to the same origin ('self').
    Uncomment the following line to apply this policy if needed.
    """
    # response.headers["Content-Security-Policy"] = "default-src 'self'"

    return response

# Load SpaCy NLP pipeline for English
nlp = spacy.load("en_core_web_sm")


# Define Pydantic model for request body
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


@app.post("/pos_tag")
async def pos_tag_text(request: TextRequest):
    """
    Tokenizes and tags parts of text for the input text using NLTK.

    Args:
        request (TextRequest): Request body containing the text to tokenize.

    Returns:
        list: List of dictionaries, each containing 'token' and 'tag' for each word/token.

    Raises:
        HTTPException: If there is an error during tokenization or if input is not a string.
    """
    try:
        tokens = nltk.word_tokenize(request.text)
        tagged_tokens = nltk.pos_tag(tokens)
        tagged_tokens_dict = [{"token": token, "tag": tag} for token, tag in tagged_tokens]
        return tagged_tokens_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to tokenize text: {str(e)}")


@app.post("/ner")
async def ner_text(request: TextRequest):
    """
    Performs Named Entity Recognition (NER) on the input text using SpaCy.
    It processes the text and identifies named entities using SpaCy's NER capabilities.

    Args:
        request (TextRequest): Request body containing the text to process for NER.

    Returns:
        list: A list of entities and their labels.
              The format is [[entity, label]] where `entity` is the
              recognized named entity and `label` is the type of the entity.

    Raises:
        HTTPException: If there is an error during NER processing, a 500 status code is returned
                       with an error message.
    """
    try:
        doc = nlp(request.text)
        entities_list = [(ent.text, ent.label_) for ent in doc.ents]

        return entities_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process text for NER: {str(e)}")


# This block will run if this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
