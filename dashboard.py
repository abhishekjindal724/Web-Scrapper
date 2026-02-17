import streamlit as st
import time
import os
from core.scraper import EcomScraper
from core.analyzer import DataAnalyzer

st.set_page_config(page_title="E-com Intel Pro", page_icon="🚀", layout="wide")

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load Custom CSS
load_css("style.css")

def render_metric_card(icon, label, value, card_class, value_style=""):
    """Renders a single premium metric card."""
    style_attr = f' style="{value_style}"' if value_style else ''
    st.markdown(f"""
        <div class="metric-card {card_class}">
            <span class="metric-icon">{icon}</span>
            <div class="metric-label">{label}</div>
            <div class="metric-value"{style_attr}>{value}</div>
        </div>
    """, unsafe_allow_html=True)

def render_sentiment_bar(score):
    """Renders a visual sentiment gauge bar."""
    # score ranges from -1 to 1, map to 0-100%
    position = int((score + 1) / 2 * 100)
    position = max(5, min(95, position)) # clamp
    
    if score > 0.3:
        label = "Positive 😊"
        color = "#10B981"
    elif score > -0.3:
        label = "Neutral 😐"
        color = "#F59E0B"
    else:
        label = "Negative 😞"
        color = "#EF4444"
    
    st.markdown(f"""
        <div class="sentiment-bar-container">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.8rem;">
                <span style="color: #9CA3AF; font-size: 0.85rem;">Sentiment Analysis</span>
                <span style="color: {color}; font-weight: 600; font-size: 0.9rem;">{label} ({score:.2f})</span>
            </div>
            <div class="sentiment-bar-bg">
                <div class="sentiment-marker" style="left: {position}%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                <span style="color: #6B7280; font-size: 0.7rem;">Negative</span>
                <span style="color: #6B7280; font-size: 0.7rem;">Neutral</span>
                <span style="color: #6B7280; font-size: 0.7rem;">Positive</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def main():
    # Hero Section
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">E-com Intel Pro</h1>
            <p class="hero-subtitle">AI-Powered Price Tracking & Sentiment Analysis</p>
        </div>
    """, unsafe_allow_html=True)

    # Search Bar
    url = st.text_input("", placeholder="🔗  Paste any Amazon product URL...", key="url_input", label_visibility="collapsed")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        scrape_btn = st.button("🔍 Analyze Product", type="primary", use_container_width=True)
    
    # Initialize session state
    if "scraped_data" not in st.session_state:
        st.session_state.scraped_data = None
        st.session_state.current_url = ""
    
    # Scrape Logic
    if scrape_btn:
        if not url:
            st.warning("⚠️ Please enter a product URL first.")
        else:
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            status_text.info("🚀 Initializing headless browser...")
            progress_bar.progress(10)
            
            scraper = None
            analyzer = DataAnalyzer()
            
            try:
                scraper = EcomScraper()
                progress_bar.progress(30)
                status_text.info("🔍 Scraping product data...")
                
                data = scraper.scrape_product(url)
                progress_bar.progress(70)
                
                if not data:
                    progress_bar.empty()
                    status_text.error("❌ Failed to scrape data. Check the URL and try again.")
                elif data.get("name") == "Unknown Product":
                    progress_bar.empty()
                    status_text.warning("🛡️ Amazon blocked this request. Try again in 60 seconds or use a different product.")
                    
                    if "debug_screenshot" in data:
                        with st.expander("🕵️ Debug View — What the scraper sees"):
                            st.image(data["debug_screenshot"], caption="Headless Browser Capture", use_container_width=True)
                    
                    st.session_state.scraped_data = data
                    st.session_state.current_url = url
                else:
                    status_text.info("🧠 Analyzing sentiment...")
                    progress_bar.progress(85)
                    
                    reviews = data.get('reviews', [])
                    sentiment_score = 0.0
                    if reviews:
                        sentiment_score = analyzer.analyze_sentiment(reviews)
                    
                    data['sentiment_score'] = sentiment_score
                    
                    st.session_state.scraped_data = data
                    st.session_state.current_url = url
                    
                    progress_bar.progress(95)
                    
                    # Save to database
                    try:
                        from core.database_manager import DatabaseManager
                        db = DatabaseManager()
                        if db.connect():
                            db.create_tables()
                            db.insert_product(data)
                            db.close()
                    except Exception as e:
                        st.toast(f"DB: {e}", icon="⚠️")
                    
                    progress_bar.progress(100)
                    time.sleep(0.3)
                    progress_bar.empty()
                    status_text.empty()

            except Exception as e:
                progress_bar.empty()
                st.error(f"❌ Error: {e}")
            finally:
                if scraper:
                    scraper.close()

    # ===== RESULTS DISPLAY =====
    if st.session_state.scraped_data:
        data = st.session_state.scraped_data
        current_url = st.session_state.current_url
        
        # Product Title
        st.markdown(f'<div class="product-title">{data.get("name", "Unknown Product")}</div>', unsafe_allow_html=True)
        
        # Show debug info if price extraction failed
        if data.get('price') == 'N/A' and 'debug_screenshot' in data:
            st.warning("⚠️ Price could not be extracted for this product. The debug view below shows what the scraper sees.")
            with st.expander("🕵️ Debug View — Price not found", expanded=True):
                st.image(data["debug_screenshot"], caption="Headless Browser Capture", use_container_width=True)
        
        # Metric Cards Row
        m1, m2, m3, m4 = st.columns(4)
        
        price_display = data.get('price', 'N/A')
        rating_display = data.get('rating', 'N/A')
        # Clean up rating display
        if rating_display and 'out of' in str(rating_display):
            rating_display = str(rating_display).split(' out')[0]
            rating_display += " ⭐"
        
        status_display = data.get('availability', 'Unknown')
        if 'stock' in str(status_display).lower():
            status_display = "In Stock"
            status_style = "color: #10B981;"
        elif 'unavailable' in str(status_display).lower():
            status_display = "Unavailable"
            status_style = "color: #EF4444;"
        else:
            status_style = ""
            
        s_score = data.get('sentiment_score', 0.0)
        s_color = "#10B981" if s_score > 0.3 else ("#F59E0B" if s_score > -0.3 else "#EF4444")
        
        with m1:
            render_metric_card("💰", "Price", price_display, "price")
        with m2:
            render_metric_card("⭐", "Rating", rating_display, "rating") 
        with m3:
            render_metric_card("📦", "Status", status_display, "status", status_style)
        with m4:
            render_metric_card("🧠", "Sentiment", f"{s_score:.2f}", "sentiment", f"color: {s_color};")
        
        # Sentiment Bar
        st.markdown("")  # spacer
        render_sentiment_bar(s_score)

        # ===== PRICE ALERT Section =====
        st.divider()
        st.markdown('<div class="section-header"><span class="icon">🔔</span> Set Price Alert</div>', unsafe_allow_html=True)
        
        with st.form("alert_form"):
            a1, a2 = st.columns(2)
            with a1:
                target_price = st.number_input("Target Price (₹)", min_value=1.0, step=10.0)
            with a2:
                email = st.text_input("Your Email")
            
            submitted = st.form_submit_button("🔔 Set Alert", use_container_width=True)
            if submitted:
                if email and target_price > 0:
                    try:
                        from core.database_manager import DatabaseManager
                        db_alert = DatabaseManager()
                        if db_alert.connect():
                            db_alert.create_tables()
                            if db_alert.add_alert(current_url, float(target_price), email):
                                st.success(f"✅ Alert set! You'll be emailed when price drops to ₹{target_price:.0f}")
                            else:
                                st.error("Failed to save alert.")
                            db_alert.close()
                        else:
                            st.error("Database connection failed.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please enter a valid email and target price.")

        # ===== REVIEWS Section =====
        st.divider()
        reviews = data.get('reviews', [])
        st.markdown(f'<div class="section-header"><span class="icon">💬</span> Customer Reviews ({len(reviews)})</div>', unsafe_allow_html=True)
        
        if reviews:
            for i, review in enumerate(reviews):
                st.markdown(f"""
                    <div class="review-card">
                        <div class="review-number">Review #{i+1}</div>
                        <div class="review-text">{review}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #6B7280;">
                    <p style="font-size: 2rem;">📝</p>
                    <p>No reviews extracted. Reviews may require scrolling or a dedicated reviews page.</p>
                </div>
            """, unsafe_allow_html=True)

        # Raw Data
        with st.expander("📊 Raw Scraped Data (JSON)"):
            st.json(data)
    
    else:
        # ===== EMPTY STATE =====
        st.markdown("""
            <div class="empty-state">
                <div class="big-icon">🔍</div>
                <h3>Ready to Analyze</h3>
                <p>Paste an Amazon product URL above and click "Analyze Product" to get started.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown("""
                <div class="metric-card price" style="text-align: center;">
                    <span class="metric-icon">🕵️</span>
                    <div class="metric-label">Smart Scraping</div>
                    <div style="color: #9CA3AF; font-size: 0.85rem; margin-top: 0.5rem;">
                        Bypasses anti-bot protections with stealth headers
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with f2:
            st.markdown("""
                <div class="metric-card rating" style="text-align: center;">
                    <span class="metric-icon">🧠</span>
                    <div class="metric-label">AI Analysis</div>
                    <div style="color: #9CA3AF; font-size: 0.85rem; margin-top: 0.5rem;">
                        NLP sentiment analysis on customer reviews
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with f3:
            st.markdown("""
                <div class="metric-card status" style="text-align: center;">
                    <span class="metric-icon">📧</span>
                    <div class="metric-label">Price Alerts</div>
                    <div style="color: #9CA3AF; font-size: 0.85rem; margin-top: 0.5rem;">
                        Automated email when prices drop to your target
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="footer">
            Built with ❤️ using Python, Selenium & Streamlit · 
            <a href="https://github.com" target="_blank">View on GitHub</a>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
