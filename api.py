from fastapi import FastAPI, Request
from pydantic import BaseModel
from models import load_model_artifacts
from utils import mask_pii_all


app = FastAPI()
model, vectorizer, label_encoder = load_model_artifacts()

class EmailRequest(BaseModel):
    email_body: str

@app.post("/")
async def classify_email(request: EmailRequest):
    original_text = request.email_body
    masked_text, entity_list = mask_pii_all(original_text)

    X = vectorizer.transform([masked_text])
    pred = model.predict(X)[0]
    category = label_encoder.inverse_transform([pred])[0]

    return {
        "input_email_body": original_text,
        "list_of_masked_entities": entity_list,
        "masked_email": masked_text,
        "category_of_the_email": category
    }