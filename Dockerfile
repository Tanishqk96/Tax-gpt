FROM python:3.11-slim

WORKDIR /app

COPY . .

# Install Python dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose the port Streamlit will run on
EXPOSE 8000

# Start Streamlit on port 8000 with CORS disabled
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8000", "--server.enableCORS=false", "--server.address=0.0.0.0"]
