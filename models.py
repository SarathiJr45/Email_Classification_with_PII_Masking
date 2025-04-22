import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from utils import load_email_data, mask_pii_all

MODEL_DIR = "saved_models/ml-email"
os.makedirs(MODEL_DIR, exist_ok=True)

def train_and_save_model(data_path: str = "data/combined_emails_with_natural_pii.csv"):
    df = load_email_data(data_path)
    df['masked_email'], _ = zip(*df['email'].map(mask_pii_all))

    label_encoder = LabelEncoder()
    df['label_encoded'] = label_encoder.fit_transform(df['type'])

    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['masked_email'])
    y = df['label_encoded']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    with open(os.path.join(MODEL_DIR, "email_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    with open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)
    with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "wb") as f:
        pickle.dump(label_encoder, f)

def load_model_artifacts():
    with open(os.path.join(MODEL_DIR, "email_model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "rb") as f:
        vectorizer = pickle.load(f)
    with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "rb") as f:
        label_encoder = pickle.load(f)
    return model, vectorizer, label_encoder

if __name__ == "__main__":
    train_and_save_model()