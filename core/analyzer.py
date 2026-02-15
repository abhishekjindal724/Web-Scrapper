import pandas as pd
from textblob import TextBlob

class DataAnalyzer:
    def clean_data(self, product_data):
        """
        Cleans the scraped data.
        """
        if not product_data:
            return None
            
        df = pd.DataFrame([product_data])
        
        # 1. Clean Name
        df['name'] = df['name'].apply(lambda x: x.strip() if isinstance(x, str) else x)
        
        # 2. Clean Price (Remove currency symbols, commas)
        # simplistic approach
        def clean_price(price_str):
            if not isinstance(price_str, str):
                return price_str
            return ''.join(c for c in price_str if c.isdigit() or c == '.')
            
        df['price'] = df['price'].apply(clean_price)
        
        # Convert back to dict
        return df.iloc[0].to_dict()

    def analyze_sentiment(self, reviews):
        """
        Analyzes the sentiment of a list of reviews.
        Returns an average score between -1.0 (Negative) and 1.0 (Positive).
        """
        if not reviews:
            return 0.0
            
        scores = []
        for text in reviews:
            if text:
                blob = TextBlob(text)
                scores.append(blob.sentiment.polarity)
        
        if not scores:
            return 0.0
            
        return sum(scores) / len(scores)
