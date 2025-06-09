FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY client/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy common library
COPY common/ /app/common/
RUN pip install -e /app/common

# Copy client code
COPY client/ /app/

# Expose the client port
EXPOSE 4810

# Run the client
CMD ["python", "src/main.py"] 