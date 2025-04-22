FROM python:3.10-slim

WORKDIR /code

# Install build tools 
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy your project files
COPY . /code

# Upgrade pip and pre-install numpy 
RUN pip install --upgrade pip && pip install "numpy<1.25.0"

# Install the  dependencies
RUN pip install -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Expose port for FastAPI
EXPOSE 7860

# Run the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
