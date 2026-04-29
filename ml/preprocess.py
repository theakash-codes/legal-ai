import pandas as pd
import re

def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_data():
    df = pd.read_csv("ml/data/legaldoc.csv", on_bad_lines='skip')

    if "text" not in df.columns:
        df.columns = ["text"]

    df["text"] = df["text"].apply(clean_text)

    return df

if __name__ == "__main__":
    df = load_data()
    print(df.head())