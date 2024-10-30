FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn
COPY client.py .

CMD ["python", "client.py"]