---
title: Email Classification & PII Masking API
emoji: 📧
colorFrom: blue
colorTo: pink
sdk: docker
app_file: app.py
pinned: false
---

# Email Classifier API with PII Masking (FastAPI)

This is a Docker-based Hugging Face Space using **FastAPI** to:

- 🔒 Mask personal information (PII) using spaCy + regex
- 🧠 Classify support emails into categories like Billing, Technical, etc.
- 📤 Return clean JSON with masked entities and classification

## How to Use

Send a POST request to `/` with:

```json
{
  "email_body": "Hello, my name is Rahul Sharma. My card is 1234-5678-1234-5678"
}
