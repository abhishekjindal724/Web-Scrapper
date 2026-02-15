import time
import sys
import io

# Fix for Windows console unicode issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from core.database_manager import DatabaseManager
from core.scraper import EcomScraper
from core.analyzer import DataAnalyzer
from config.settings import HEADLESS

def main():
    print("Starting AI-Ready E-commerce Intelligence Tool...")

    # 1. Initialize Components
    print("Initializing Database...")
    db = DatabaseManager()
    if not db.connect():
        print("WARNING: Failed to connect to database. Data will NOT be saved.")
        print("Please check your MySQL settings in config/settings.py")
        # We continue without DB for demonstration purposes
    else:
        db.create_tables()
    
    print("Initializing Scraper...")
    try:
        scraper = EcomScraper()
    except Exception as e:
        print(f"Error initializing scraper: {e}")
        return

    analyzer = DataAnalyzer()

    # 2. Define Target URLs (These are examples)
    # You can add real product URLs here.
    urls = [
         "https://www.amazon.in/Cetaphil-Hydrating-Sulphate-Free-Niacinamide-Sensitive/dp/B01CCGW4OE/ref=zg_bs_c_beauty_d_sccl_2/525-9900189-6246244", 
    ]

    try:
        for url in urls:
            print(f"\nProcessing: {url}")
            
            # 3. Scrape
            raw_data = scraper.scrape_product(url)
            if not raw_data:
                print("Failed to scrape data.")
                continue

            print(f"Raw Data Extracted: {raw_data}")

            # 4. Process & Analyze
            cleaned_data = analyzer.clean_data(raw_data)
            
            # Real Sentiment Analysis
            reviews = raw_data.get('reviews', [])
            print(f"Analyzing {len(reviews)} reviews...")
            sentiment_score = analyzer.analyze_sentiment(reviews)
            
            cleaned_data['sentiment_score'] = sentiment_score
            cleaned_data['reviews_count'] = len(reviews) # Adding this for context, though not in DB schema yet 

            print(f"Cleaned Data: {cleaned_data}")
            print(f"Sentiment Analysis Score: {sentiment_score} (Positive > 0, Negative < 0)")

            # 5. Save to Database
            if db.conn:
                db.insert_product(cleaned_data)
            else:
                print("Skipping DB save (No connection).")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # 6. Cleanup
        print("\nCleaning up resources...")
        if 'scraper' in locals():
            scraper.close()
        if 'db' in locals():
            db.close()
        print("Job Complete.")

if __name__ == "__main__":
    main()
