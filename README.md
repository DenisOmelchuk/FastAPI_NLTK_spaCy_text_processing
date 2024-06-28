
# FastAPI NLTK spaCy Text Processing Application

This application provides text processing functionalities using FastAPI, NLTK, and spaCy. It includes endpoints for tokenization, part-of-speech tagging, and named entity recognition.




## Deployment

### 1. Using git clone
Steps:

1: Create a virtual environment: 

    python -m venv venv

2: Clone the project:

    git clone https://github.com/DenisOmelchuk/FastAPI_NLTK_spaCy_text_processing.git

    cd FastAPI_NLTK_spaCy_text_processing

3: Activate the virtual environment:

• Windows:

    venv/Scripts/activate

• macOS/Linux:

    source venv/bin/activate


4: Install dependencies:

    pip install -r requirements.txt

5: Run the application:

    uvicorn main:app --reload --host 127.0.0.1 --port 8000

The application should now be running on http://127.0.0.1:8000.

### 2. Using Docker

Open terminal and run:

    docker run -p 8000:8000 denysomelchuk/fast_api_nltk_spacy_text_processing:latest

The application should now be running on http://127.0.0.1:8000.


## List of Endpoints

### Request Format
All requests to this API must be made using the POST method. The API expects the request body to be in JSON format.

### Tokenization

• URL: http://127.0.0.1:8000/tokenize/

• Description: Tokenizes the input text using NLTK's word_tokenize function.

• Request:

    {
    "text": "Your input text here."
    }

• Response:

    ["List", "of", "tokens"]


### Part-of-Speech Tagging

• URL: http://127.0.0.1:8000/pos_tag/

• Description: Tokenizes and tags parts of speech for the input text using NLTK.

• Request:

    {
    "text": "Your input text here."
    }

• Response:

    [{"tag": "POS_tag"}]


### Named Entity Recognition

• URL: http://127.0.0.1:8000/ner/

• Description: Processes the text and identifies named entities using spaCy's NER capabilities.

• Request:

    {
    "text": "Your input text here."
    }

• Response:

    [["entity", "label"]]


## Notes

•  The API server accepts HTTPS requests only. To change this, comment out line 25 in main.py

    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

• Content Security Policy is not active. To activate it, uncomment line 33 in main.py

    response.headers["Content-Security-Policy"] = "default-src 'self'"

## Testing

Tests are implemented using Pytest and Pytest Asyncio, covering all functionalities of the application.

To run tests:

    pytest








