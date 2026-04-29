import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import pandas as pd
import numpy as np
import pickle
import re
import mlflow
import mlflow.keras

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ---------- CLEAN FUNCTION ----------
def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ---------- LOAD DATA ----------
df = pd.read_csv("ml/data/legaldoc.csv", on_bad_lines='skip')

texts = df.iloc[:, 0].astype(str)
texts = texts.apply(clean_text)

# ---------- TOKENIZER ----------
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(texts)

X = tokenizer.texts_to_sequences(texts)
X = pad_sequences(X, maxlen=50)

X = np.array(X).astype("float32")

# ---------- LABELS ----------
y = np.ones((len(X), 1)).astype("float32")

# ---------- MODEL ----------
model = Sequential([
    Embedding(5000, 64),
    LSTM(32),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam')

# ---------- MLFLOW TRACKING ----------
mlflow.set_experiment("Legal_AI_LSTM")

with mlflow.start_run():

    print("🚀 Training started...")

    history = model.fit(X, y, epochs=2, batch_size=16)

    # ---------- LOG PARAMETERS ----------
    mlflow.log_param("epochs", 2)
    mlflow.log_param("batch_size", 16)
    mlflow.log_param("max_len", 50)

    # ---------- LOG METRICS ----------
    final_loss = history.history['loss'][-1]
    mlflow.log_metric("loss", final_loss)

    # ---------- SAVE MODEL ----------
    model.save("ml/models/model.keras")

    # ---------- LOG MODEL ----------
    mlflow.keras.log_model(model, "model")

    # ---------- SAVE TOKENIZER ----------
    with open("ml/tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)

    mlflow.log_artifact("ml/tokenizer.pkl")

    print("✅ LSTM model trained & logged with MLflow!")