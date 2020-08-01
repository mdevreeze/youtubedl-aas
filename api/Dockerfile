FROM tiangolo/uvicorn-gunicorn-fastapi
RUN apt update && apt install gifsicle

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV APP_MODULE="api.main:app"

COPY ./ /app/api
