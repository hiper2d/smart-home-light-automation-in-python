FROM python:3.11-slim

WORKDIR /app

COPY docker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

EXPOSE 5001

CMD ["python", "echo.py"]