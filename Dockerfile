FROM python:3.11-slim

WORKDIR /app

COPY . .

# Skip gcc — try to install only Python deps
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
