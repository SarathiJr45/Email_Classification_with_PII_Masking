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

**Example**:

```json
{
  "email_body": "Hello, my name is Partha Sarathi. I was born on 29/07/2003. My Aadhar number is 1234 5678 9101 and my registered email is sarathi@gmail.com. You can contact me at 9876543210. My card number is 1234-5678-9012-3456, CVV is 123 and expiry date is 06/25. Please update my billing preferences accordingly"
}

 Response Format:

 {
  "input_email_body": "Hello, my name is Partha Sarathi. I was born on 29/07. My Aadhar number is 123456789101 and my registered email is sarathi@gmail.com. You can contact me at +919876543210. My card number is 12345678-90123456, CVV is 123 and expiry date is 6/25. Please update my billing preferences accordingly",
  "list_of_masked_entities": [
    {
      "position": [
        18,
        32
      ],
      "classification": "full_name",
      "entity": "Partha Sarathi"
    },
    {
      "position": [
        75,
        87
      ],
      "classification": "aadhar_num",
      "entity": "123456789101"
    },
    {
      "position": [
        115,
        132
      ],
      "classification": "email",
      "entity": "sarathi@gmail.com"
    },
    {
      "position": [
        156,
        169
      ],
      "classification": "phone_number",
      "entity": "+919876543210"
    },
    {
      "position": [
        189,
        206
      ],
      "classification": "credit_debit_no",
      "entity": "12345678-90123456"
    },
    {
      "position": [
        208,
        218
      ],
      "classification": "cvv_no",
      "entity": "CVV is 123"
    }
  ],
  "masked_email": "Hello, my name is [full_name]. I was born on 29/07. My Aadhar number is [aadhar_num] and my registered email is [email]. You can contact me at [phone_number]. My card number is [credit_debit_no], [cvv_no] and expiry date is 6/25. Please update my billing preferences accordingly",
  "category_of_the_email": "Change"
}
