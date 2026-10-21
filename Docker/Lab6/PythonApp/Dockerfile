# Base image: Official lightweight Python 3.12 slim Debian variant
FROM python:3.12-slim

# Set container working directory:
WORKDIR /app

# Copy dependency list:
COPY requirements.txt .

# Install dependencies:
#   --no-cache-dir: Prevents pip from caching downloaded wheel files inside ~/.cache, saving layer disk space
#   -r requirements.txt: Specifies requirements file to parse
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code:
COPY app.py .

# Expose web application port:
EXPOSE 5000

# JSON exec form starts Python application directly:
CMD ["python", "app.py"]
