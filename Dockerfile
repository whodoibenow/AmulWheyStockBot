FROM ghcr.io/puppeteer/puppeteer:latest

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Set Python alias
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY main.py .

# Run your bot
CMD ["python", "main.py"]
