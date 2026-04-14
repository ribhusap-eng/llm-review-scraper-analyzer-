import pandas as pd

df = pd.read_csv("steam_reviews.csv")

# remove missing and very short reviews
df["review_text"] = df["review_text"].astype(str).str.strip()
df = df[df["review_text"].notna()]
df = df[df["review_text"].str.len() >= 10]

# optional: remove duplicate reviews again just to be safe
df = df.drop_duplicates(subset=["review_date", "rating", "username", "review_text"])

df.to_csv("steam_reviews_cleaned.csv", index=False, encoding="utf-8-sig")

print("Final cleaned rows:", len(df))