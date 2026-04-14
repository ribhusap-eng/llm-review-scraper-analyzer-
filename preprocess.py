import pandas as pd
import re

INPUT_FILE = "steam_reviews_cleaned.csv"
OUTPUT_FILE = "steam_reviews_processed.csv"

def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text)
    text = text.encode("utf-8", "ignore").decode("utf-8")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[^\w\s.,!?'-]", "", text)
    return text

def preprocess_reviews():
    df = pd.read_csv(INPUT_FILE)

    df["review_text"] = df["review_text"].apply(clean_text)
    df = df[df["review_text"].str.len() > 0]
    df = df.drop_duplicates(subset=["review_text"])

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Processed file saved as {OUTPUT_FILE}")
    print(f"Total reviews after preprocessing: {len(df)}")

if __name__ == "__main__":
    preprocess_reviews()