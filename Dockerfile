FROM python:3.10-slim

WORKDIR /code

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY . /code

# Fix numpy first
RUN pip install --upgrade pip && pip install "numpy<1.25.0"

# Now install everything else
RUN pip install -r requirements.txt

# Download the spaCy model
RUN python -m spacy download en_core_web_sm

# (Optional) Re-train model inside container to avoid pickle incompatibilities
# RUN python models.py

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
