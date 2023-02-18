# Pull base image
FROM python:3.10-slim-buster as builder
# Set environment variables
COPY requirements.txt requirements.txt

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


FROM builder as final
WORKDIR /app

COPY . .
CMD [ "uvicorn", "app:app", "--host", "0.0.0.0" ]