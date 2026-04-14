import os
import time
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# File paths
INPUT_FILE = "steam_reviews_processed.csv"
OUTPUT_FILE = "steam_reviews_llm_output.csv"

# Model name (OpenRouter model)
MODEL_NAME = "meta-llama/llama-3-8b-instruct"

# OpenRouter client setup
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def analyze_review(review_text):
    prompt = f"""
You are analyzing a Steam game review.

Return ONLY valid JSON in this exact format:
{{
  "sentiment": "Positive/Negative/Neutral",
  "summary": "Short one-line summary"
}}

Review:
{review_text}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a review analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()
        parsed = json.loads(content)

        return {
            "llm_sentiment": parsed.get("sentiment", ""),
            "llm_summary": parsed.get("summary", ""),
            "status": "success"
        }

    except Exception as e:
        return {
            "llm_sentiment": "",
            "llm_summary": "",
            "status": f"error: {str(e)}"
        }

def run_llm_analysis():
    df = pd.read_csv(INPUT_FILE)

    # Optional: limit rows for faster demo/testing
    # df = df.head(50)

    sentiments = []
    summaries = []
    statuses = []

    for i, row in df.iterrows():
        print(f"Processing review {i+1}/{len(df)}")

        result = analyze_review(str(row["review_text"]))

        sentiments.append(result["llm_sentiment"])
        summaries.append(result["llm_summary"])
        statuses.append(result["status"])

        time.sleep(1)

    df["llm_sentiment"] = sentiments
    df["llm_summary"] = summaries
    df["status"] = statuses

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved final file: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_llm_analysis()