FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our source code and the saved brain (model)
COPY src/ ./src/
COPY model/ ./model/

EXPOSE 8000

# Start the API
CMD ["python", "src/app.py"]