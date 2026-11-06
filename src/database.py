import sqlite3
import pandas as pd


def save_to_database(df):

    # Connect to SQLite database
    connection = sqlite3.connect("database/news.db")

    # Save DataFrame into database table
    df.to_sql(
        "articles",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print("News successfully saved to SQLite Database!")
    
def read_from_database():

    connection = sqlite3.connect("database/news.db")

    query = "SELECT * FROM articles"

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df    
    
    
    
    
    
    
    
    
    
    
    