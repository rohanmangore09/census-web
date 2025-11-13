FROM python:3.11-slim

WORKDIR /app
COPY backend/ /app/

RUN pip install flask flask_sqlalchemy psycopg2-binary

CMD ["python", "app.py"]
