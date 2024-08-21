FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.5.1

RUN mkdir /app/

WORKDIR /app/

COPY . .

RUN poetry install --no-root

EXPOSE 8080

ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]