# TeachXR - Backend for Database Setup
To run the API server:

## Setup the Python Virtual Environment:

`python -m venv env` (create a virtual environment)

`env/Scripts/activate` (or a similar command to start a Python virtual env on a different OS)

`pip install -r requirements.txt` (install requirements. sorry since there are a lot of unused libs in there!)

## Setup Google Cloud Services

Add a folder 'keys' to your top-level folder.

In there, add your Google Cloud Services json key file in there, and put its path in .env in this format:

GOOGLE_APPLICATION_CREDENTIALS=<your path here>

## Run the Python Server

`python src/server.py` (or a similar command to run a Python script on a different OS)