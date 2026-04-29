# ⚖️ LegalAI Pro — AI Legal Document Assistant

LegalAI Pro is an intelligent legal document assistant that uses machine learning to summarize documents, detect risks, identify fraud patterns, and provide simplified legal insights through an interactive web interface.

---

## 🚀 Features

- 📄 Document Upload (PDF, DOCX, TXT)
- 🧠 AI Summary Generation
- ⚠️ Risk Analysis
- 🔍 Fraud Detection
- ✅ Compliance Checking
- 📖 Legal Simplification
- 💬 AI Chat Assistant
- 🌐 Translation
- 🧑‍⚖️ Lawyer Recommendations
- 📊 Analytics Dashboard

---

## 🧠 Machine Learning

- LSTM-based model for legal text classification  
- Tokenization and sequence modeling  
- Integrated with Django backend for real-time predictions  
- Supports MLOps pipeline  

---

## 🤖 Machine Learning Models

This project uses deep learning for analyzing legal documents.

### 🔹 Model Used
- LSTM (Long Short-Term Memory)
- Built using TensorFlow / Keras

### 🔹 Input Processing
- Text cleaning
- Tokenization
- Padding sequences

### 🔹 Output
- Risk prediction / legal insights

### 🔹 Model Files
- `ml/models/model.keras`
- `ml/tokenizer.pkl`

### 🔹 Training Pipeline
- Dataset → preprocessing → training → saved model

### 🔹 MLOps Integration
- `ml/train.py` → training pipeline
- `ml/predict.py` → inference system

---

## 🛠️ Tech Stack

### Backend
- Django
- Django REST Framework

### Frontend
- HTML, CSS, JavaScript

### ML
- TensorFlow / Keras

### DevOps / MLOps
- Docker
- MLflow
- GitHub

---

## ⚙️ Setup

```bash
pip install -r requirements.txt
python ml/train.py
python manage.py runserver