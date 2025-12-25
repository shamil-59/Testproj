FROM python:3.11-slim

WORKDIR /app
COPY ./src ./src
COPY ./book ./book
RUN pip install --upgrade pip
RUN pip install uvicorn fastapi pydantic aiofiles

CMD ["python3", "src/main.py"]