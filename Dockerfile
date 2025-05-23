FROM python:3.7.9-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8080

CMD ["uvicorn", "library.main:app", "--host", "0.0.0.0", "--port", "8080"]


