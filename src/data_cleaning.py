import pandas as pd
from collections import Counter
import re

def clean_news_data(df):

    print("Original Dataset Shape:", df.shape)

    # Remove duplicate articles using link
    df = df.drop_duplicates(subset=["link"])

    # Remove rows with missing title or link
    df = df.dropna(subset=["title", "link"])

    # Remove empty titles and links
    df = df[
        (df["title"].str.strip() != "") &
        (df["link"].str.strip() != "")
    ]

    print("Cleaned Dataset Shape:", df.shape)

    return df


def extract_keywords(df):

    all_titles = " ".join(df["title"].dropna()).lower()

    words = re.findall(r"\b[a-z]{3,}\b", all_titles)

    stopwords = {
        "the", "and", "for", "with", "from",
        "that", "this", "has", "have", "are",
        "was", "will", "its", "into", "after"
    }

    filtered_words = [
        word for word in words
        if word not in stopwords
    ]

    keyword_counts = Counter(filtered_words)

    return keyword_counts.most_common(10)