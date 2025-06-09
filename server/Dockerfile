FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy common library
COPY common/ /app/common/
RUN pip install -e /app/common

# Copy server code
COPY server/ /app/

# Expose the server port
EXPOSE 4800

# Run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4800"] 