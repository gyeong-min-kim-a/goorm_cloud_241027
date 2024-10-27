FROM python:3.12.3-slim

RUN pip install poetry==1.8.3

COPY . . 

RUN poetry install 

ENTryPOINT ['poetry','run','uvicorn','min:app']