## AI Engineer Intern Assignment 2: LLM Review Scraper & Analyzer

## Project Overview
This project is an end-to-end Python application that scrapes customer reviews from a public product page, preprocesses the collected text, and uses an OpenAI-compatible Large Language Model (LLM) to generate structured insights such as sentiment and concise summaries.

The solution demonstrates practical implementation of:
- Web scraping
- Data preprocessing
- API integration
- Text analytics
- Error handling
- Structured data storage

---

## Objective
To build a robust Python pipeline that:

1. Takes a product review page URL as input  
2. Scrapes customer reviews and metadata  
3. Cleans and preprocesses review text  
4. Sends processed reviews to an OpenAI-compatible API  
5. Generates sentiment analysis and concise summaries  
6. Stores final results in a structured output file

---

## Selected Product Source
**Platform:** Steam  
**Product:** The Witcher 3: Wild Hunt  
**App ID:** 292030

Steam was selected because:
- Reviews are publicly visible
- Metadata is structured and accessible
- Suitable for pagination and bulk scraping
- Ideal for NLP and sentiment analysis tasks

---

## Workflow

```text
Input URL
   ↓
scraper.py
   ↓
Raw Reviews CSV
   ↓
preprocess.py
   ↓
Cleaned Reviews CSV
   ↓
llm_analyzer.py
   ↓
LLM Sentiment + Summary
   ↓
Final Output CSV

git clone <your-repository-link>
cd LLM-Review-Project
pip install -r requirements.txt