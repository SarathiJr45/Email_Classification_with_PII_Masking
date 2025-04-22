FROM python:3.10-slim

WORKDIR /code

# Install system build tools (required by numpy + sklearn)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy source code into container
COPY . /code

# Upgrade pip and pre-install compatible numpy
RUN pip install --upgrade pip && pip install "numpy<1.25.0"

# Install project dependencies
RUN pip install -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# ⚠️ Re-train model inside container (avoid loading .pkl files)
RUN python models.py

# Expose default FastAPI port
EXPOSE 7860

# Launch FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
