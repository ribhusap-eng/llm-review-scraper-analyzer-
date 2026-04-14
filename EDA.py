import pandas as pd

df = pd.read_csv("steam_reviews_cleaned.csv")

# review length
df["char_count"] = df["review_text"].astype(str).apply(len)
df["word_count"] = df["review_text"].astype(str).apply(lambda x: len(x.split()))

# sentiment numeric
df["sentiment"] = df["rating"].map({"Positive":1, "Negative":0})

print(df.head())

import matplotlib.pyplot as plt

#Barplot: Positive vs Negative
df["rating"].value_counts().plot(kind="bar")
plt.title("Review Sentiment Distribution")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()

#Histogram: Positive vs Negative
df["word_count"].hist(bins=30)
plt.title("Distribution of Review Length")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.show()

#Most common Word
from collections import Counter
import re

text = " ".join(df["review_text"].astype(str)).lower()
words = re.findall(r'\b[a-z]+\b', text)

common = Counter(words).most_common(20)
print(common)

#Positive vs Negative Review Length
print(df.groupby("rating")["word_count"].mean())