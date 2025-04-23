import pandas as pd
import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def load_email_data(file_path: str):
    df = pd.read_csv(file_path)
    df.dropna(subset=['email', 'type'], inplace=True)
    df['email'] = df['email'].str.replace("Subject:", "", regex=False).str.strip()
    return df

def mask_pii_all(text):
    entity_list = []
    replacements = []

    patterns = {
        "email": r'\b[\w\.-]+@[\w\.-]+\.\w+\b',
        "phone_number": r'(?:(?:\+91|91|0)?[\s\-]?)?[6-9]\d{9}',
        "aadhar_num": r'\b\d{4}\s*\d{4}\s*\d{4}\b',
        "credit_debit_no": r'\b(?:\d{4}[ -]?){3}\d{4}\b',
        "cvv_no": r'\bCVV[:\s\-]*\d{3,4}\b|\b\d{3,4}(?=\s*CVV)',
        "expiry_no": r'\b(0[1-9]|1[0-2])[/\-](\d{2}|\d{4})\b',
        "dob": r'\b(?:\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})|(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[.\s-]\d{1,2}[,.\s-]\d{2,4})\b'
    }

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            tokens = ent.text.strip().split()
            if any(tok.lower() in {"card", "cvv", "expiry"} for tok in tokens):
                continue
            if re.search(r'\d', ent.text):
                continue
            replacements.append((ent.start_char, ent.end_char, "full_name", ent.text)

    for label, pattern in patterns.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            replacements.append((match.start(), match.end(), label, match.group()))

    replacements.sort(key=lambda x: (x[0], -x[1]))
    non_overlapping = []
    for current in replacements:
        if not any(max(current[0], r[0]) < min(current[1], r[1]) for r in non_overlapping):
            non_overlapping.append(current)

    masked_text = ""
    prev_end = 0
    for start, end, label, original in non_overlapping:
        masked_text += text[prev_end:start] + f"[{label}]"
        entity_list.append({
            "position": [start, end],
            "classification": label,
            "entity": original
        })
        prev_end = end
    masked_text += text[prev_end:]

    return masked_text, entity_list