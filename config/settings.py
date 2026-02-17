import os

# Try to load from Streamlit secrets first (for Streamlit Cloud),
# then fall back to environment variables (for GitHub Actions / local runs)

try:
    import streamlit as st
    DB_HOST = st.secrets["DB_HOST"]
    DB_USER = st.secrets["DB_USER"]
    DB_PASSWORD = st.secrets["DB_PASSWORD"]
    DB_NAME = st.secrets["DB_NAME"]
except Exception:
    # Catches: ImportError, StreamlitAPIException, KeyError, FileNotFoundError, etc.
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "") 
    DB_NAME = os.getenv("DB_NAME", "ecommerce_db")
    
# SSL Configuration (Required for most Cloud DBs like TiDB/Aiven)
DB_SSL = {"ssl_disabled": False} if os.getenv("DB_SSL", "True") == "True" else {}

# Scraper Configuration
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# Random delay range between requests (in seconds)
DELAY_RANGE = (2, 5) 

# For headless mode (no UI)
HEADLESS = True

# Email Credentials
try:
    import streamlit as st
    EMAIL_SENDER = st.secrets.get("EMAIL_SENDER", "abhishekjindal724@gmail.com")
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
except Exception:
    EMAIL_SENDER = os.getenv("EMAIL_SENDER", "abhishekjindal724@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

