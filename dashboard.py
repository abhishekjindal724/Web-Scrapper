import streamlit as st
import time
import os
from core.scraper import EcomScraper
from core.analyzer import DataAnalyzer

st.set_page_config(page_title="E-com Intel Tool", page_icon="🛒", layout="wide")

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load Custom CSS
load_css("style.css")

def main():
    # Hero Section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 class='title-animate' style='font-size: 3rem; margin-bottom: 0.5rem;'>🚀 E-com Intel <span style='color: #FF4B4B;'>Pro</span></h1>
            <p style='color: #A0A0A0; font-size: 1.2rem;'>AI-Powered Price Tracking & Sentinel Analysis</p>
        </div>
    """, unsafe_allow_html=True)

    # Input Section (Card Style)
    st.markdown("<div style='background: rgba(255,255,255,0.02); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;'>", unsafe_allow_html=True)
    url = st.text_input("", placeholder="Paste Amazon Product URL here...", key="url_input", label_visibility="collapsed")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        scrape_btn = st.button("🔍 Analyze Product", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Initialize session state for data
    if "scraped_data" not in st.session_state:
        st.session_state.scraped_data = None
        st.session_state.current_url = ""
    
    if scrape_btn:
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
                elif data.get("name") == "Unknown Product":
                    status_text.warning("⚠️ Amazon blocked the request (Anti-Bot). Try again in a few seconds or use a different product.")
                    
                    # Show Debug Screenshot if available
                    if "debug_screenshot" in data:
                        st.subheader("🕵️ Debug View (What the scraper sees):")
                        st.image(data["debug_screenshot"], caption="Headless Browser View", use_container_width=True)
                    
                    st.session_state.scraped_data = data
                    st.session_state.current_url = url
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
        
        st.markdown(f"### {data.get('name', 'Unknown Product')}")
        
        # Modern Metric Cards
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        
        with m_col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Price</div>
                    <div class="metric-value">{data.get('price', 'N/A')}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with m_col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Rating</div>
                    <div class="metric-value">{data.get('rating', 'N/A')}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with m_col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Status</div>
                    <div class="metric-value" style="font-size: 1.2rem;">{data.get('availability', 'Unknown')}</div>
                </div>
            """, unsafe_allow_html=True)

        with m_col4:
            s_score = data.get('sentiment_score', 0.0)
            color = "#00FF00" if s_score > 0 else "#FF4B4B"
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Sentiment</div>
                    <div class="metric-value" style="color: {color};">{s_score:.2f}</div>
                </div>
            """, unsafe_allow_html=True)

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
