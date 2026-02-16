import streamlit as st
import time
from core.scraper import EcomScraper
from core.analyzer import DataAnalyzer

st.set_page_config(page_title="E-com Intel Tool", page_icon="🛒", layout="wide")

def main():
    st.title("🛒 AI-Ready E-commerce Intelligence Tool")
    st.markdown("Enter a product URL (""Amazon preferred"") to extract data, reviews, and sentiment analysis.")

    # Input Section
    url = st.text_input("Product URL", placeholder="https://www.amazon.in/...", key="url_input")
    
    # Initialize session state for data
    if "scraped_data" not in st.session_state:
        st.session_state.scraped_data = None
    
    if st.button("Scrape & Analyze", type="primary"):
        if not url:
            st.warning("Please enter a URL first.")
        else:
            status_text = st.empty()
            status_text.info("🚀 Initializing Scraper... (This may take a few seconds)")
            
            # Initialize components
            scraper = None
            analyzer = DataAnalyzer()
            
            try:
                scraper = EcomScraper()
                status_text.info(f"Scraping {url}...")
                
                data = scraper.scrape_product(url)
                
                if not data:
                    status_text.error("Failed to scrape data. Check the URL.")
                else:
                    status_text.success("Scraping Complete!")
                    time.sleep(0.5)
                    status_text.empty()

                    reviews = data.get('reviews', [])
                    sentiment_score = 0.0
                    if reviews:
                        sentiment_score = analyzer.analyze_sentiment(reviews)
                    
                    data['sentiment_score'] = sentiment_score
                    
                    st.session_state.scraped_data = data
                    st.session_state.current_url = url

                    try:
                        from core.database_manager import DatabaseManager
                        db = DatabaseManager()
                        if db.connect():
                            db.create_tables()
                            db.insert_product(data)
                            db.close()
                    except Exception as e:
                        st.error(f"Failed to save data: {e}")

            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if scraper:
                    scraper.close()

    # Display Results (Outside button block, depends on session state)
    if st.session_state.scraped_data:
        data = st.session_state.scraped_data
        current_url = st.session_state.current_url
        
        # Header Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Price", data.get('price', 'N/A'))
        with col2:
            st.metric("Rating", data.get('rating', 'N/A'))
        with col3:
            st.metric("Availability", data.get('availability', 'Unknown'))
        with col4:
            sentiment_score = data.get('sentiment_score', 0.0)
            st.metric("Sentiment Score", f"{sentiment_score:.2f}", delta="Positive" if sentiment_score > 0 else "Neutral/Negative")

        st.subheader(data.get('name', 'Unknown Product'))

        # --- Price Alert Section ---
        st.divider()
        st.subheader("🔔 Set Price Alert")
        with st.form("alert_form"):
            col_alert1, col_alert2 = st.columns(2)
            with col_alert1:
                target_price = st.number_input("Target Price (₹)", min_value=1.0, step=10.0)
            with col_alert2:
                email = st.text_input("Your Email")
            
            submitted = st.form_submit_button("Set Alert")
            if submitted:
                if email and target_price > 0:
                    try:
                        from core.database_manager import DatabaseManager
                        db_alert = DatabaseManager()
                        if db_alert.connect():
                            db_alert.create_tables() # Ensure tables exist
                            if db_alert.add_alert(current_url, float(target_price), email):
                                st.success(f"Alert set for ₹{target_price} to {email}!")
                            else:
                                st.error("Failed to save alert.")
                            db_alert.close()
                        else:
                            st.error("Database connection failed.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please enter a valid email and target price.")

        # Reviews Section
        st.divider()
        reviews = data.get('reviews', [])
        st.subheader(f"📝 Reviews ({len(reviews)})")
        
        if reviews:
            for i, review in enumerate(reviews):
                with st.expander(f"Review #{i+1}"):
                    st.write(review)
        else:
            st.info("No reviews extracted matching criteria.")

        # Raw Data Section
        with st.expander("📊 View Raw Data (JSON)"):
            st.json(data)

if __name__ == "__main__":
    main()
