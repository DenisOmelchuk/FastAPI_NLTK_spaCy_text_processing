from fastapi import FastAPI
from nltk_setup import download_nltk_data_packages
from contextlib import asynccontextmanager

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    During the startup event, it ensures that all required NLTK packages are downloaded
    by calling the download_nltk_data_packages() function.
    """
    download_nltk_data_packages()
    yield

app.router.lifespan_context = lifespan
