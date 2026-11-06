from src.scraper import fetch_news
from src.data_cleaning import clean_news_data
from src.database import save_to_database, read_from_database
import pandas as pd
from src.data_cleaning import clean_news_data, extract_keywords
import matplotlib.pyplot as plt
import seaborn as sns


# Step 1: Fetch news
articles = fetch_news()
df = pd.DataFrame(articles)

# Step 2: Clean data
cleaned_df = clean_news_data(df)

# Step 3: Save CSV
cleaned_df.to_csv(
    "data/cleaned_tech_news.csv",
    index=False,
    encoding="utf-8-sig"
)

# Step 4: Save database
save_to_database(cleaned_df)

# Step 5: Read database
stored_df = read_from_database()

print("\nDatabase Verification:")
print("Total Stored Articles:", len(stored_df))

print("\nStored Articles Preview:")
print(stored_df[["source", "title"]].head())

# Step 6: Keyword Analysis
top_keywords = extract_keywords(stored_df)

print("\nTop 10 Trending Keywords:")

for keyword, count in top_keywords:
    print(keyword, ":", count)
    
# Step 7: Keyword Visualization

keywords_df = pd.DataFrame(
    top_keywords,
    columns=["Keyword", "Frequency"]
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=keywords_df,
    x="Frequency",
    y="Keyword"
)

plt.title("Top 10 Technology Keywords", fontsize=16)
plt.xlabel("Frequency")
plt.ylabel("Keywords")

plt.tight_layout()
plt.savefig("data/top_keywords.png", dpi=300)
plt.show()

print("Keyword chart saved successfully!")    
    
    