FROM python:3.11-slim

# Install Chrome
COPY install_chrome.sh /install_chrome.sh
RUN chmod +x /install_chrome.sh && /install_chrome.sh

# Set display for headless chrome
ENV DISPLAY=:99

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script
COPY main.py .

# Run the script
CMD ["python", "main.py"]
