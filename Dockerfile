
FROM python:3.9


WORKDIR /app


COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .


ENV PORT 8000


EXPOSE $PORT


CMD ["./wait-for-it.sh", "db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
