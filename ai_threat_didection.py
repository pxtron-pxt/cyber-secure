import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from pathlib import Path
import joblib
from typing import Tuple, Union

# Configure VS Code-friendly settings
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)

# Constants
MODEL_PATH = Path("threat_detection_model.pkl")
VECTORIZER_PATH = Path("vectorizer.pkl")

def load_data() -> pd.DataFrame:
    """Load sample log data with labels"""
    return pd.DataFrame([
        {"log": "User failed to authenticate", "label": "threat"},
        {"log": "Connection established from IP 192.168.1.1", "label": "normal"},
        {"log": "Multiple failed login attempts", "label": "threat"},
        {"log": "User logged in from IP 192.168.1.100", "label": "normal"},
        {"log": "Suspicious activity detected on server 12", "label": "threat"},
        {"log": "Data read operation performed by user", "label": "normal"},
        {"log": "System rebooted unexpectedly", "label": "threat"},
        {"log": "Normal system operation detected", "label": "normal"}
    ])

def preprocess_data(df: pd.DataFrame) -> Tuple[CountVectorizer, np.ndarray]:
    """Convert text data to numerical features"""
    vectorizer = CountVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["log"])
    return vectorizer, X

def train_model(X: np.ndarray, y: pd.Series) -> MultinomialNB:
    """Train and return a Naive Bayes classifier"""
    model = MultinomialNB()
    model.fit(X, y)
    return model

def save_artifacts(model: MultinomialNB, vectorizer: CountVectorizer) -> None:
    """Save model and vectorizer to disk"""
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Vectorizer saved to {VECTORIZER_PATH}")

def load_artifacts() -> Tuple[MultinomialNB, CountVectorizer]:
    """Load pretrained model and vectorizer"""
    return (
        joblib.load(MODEL_PATH),
        joblib.load(VECTORIZER_PATH)
    )

class ThreatDetector:
    """Class wrapper for threat detection functionality"""
    
    def __init__(self, model: MultinomialNB = None, vectorizer: CountVectorizer = None):
        self.model = model
        self.vectorizer = vectorizer
    
    def train_new_model(self, df: pd.DataFrame) -> None:
        """Train and store a new model from DataFrame"""
        self.vectorizer, X = preprocess_data(df)
        y = df["label"]
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.25, random_state=42)
        self.model = train_model(X_train, y_train)
        save_artifacts(self.model, self.vectorizer)
    
    def load_pretrained(self) -> None:
        """Load pretrained model and vectorizer"""
        self.model, self.vectorizer = load_artifacts()
    
    def detect_threat(self, log_text: str) -> str:
        """Make prediction on new log entry"""
        if not self.model or not self.vectorizer:
            raise ValueError("Model not loaded. Train or load a model first.")
            
        new_log_vector = self.vectorizer.transform([log_text])
        prediction = self.model.predict(new_log_vector)
        return "Threat detected!" if prediction[0] == "threat" else "No threat detected."

def main():
    # Load and prepare data
    df = load_data()
    print("Sample data:")
    print(df.head())
    
    # Initialize detector
    detector = ThreatDetector()
    
    # Check for existing model
    if MODEL_PATH.exists() and VECTORIZER_PATH.exists():
        detector.load_pretrained()
        print("\nLoaded pretrained model")
    else:
        print("\nTraining new model...")
        detector.train_new_model(df)
    
    # Example predictions
    test_logs = [
        "Suspicious IP address accessed the system",
        "Regular user login detected",
        "Unauthorized database access attempt"
    ]
    
    print("\nTest predictions:")
    for log in test_logs:
        print(f"{log}: {detector.detect_threat(log)}")

if __name__ == "__main__":
    main()
    