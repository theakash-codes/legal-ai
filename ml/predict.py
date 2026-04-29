from tensorflow.keras.models import load_model

try:
    model = load_model("ml/models/model.keras")
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Model loading failed:", e)
    model = None


def predict_text(text):
    if model is None:
        return "Model not loaded"

    return "AI Legal Analysis Result"