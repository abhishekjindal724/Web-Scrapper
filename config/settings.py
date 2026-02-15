import os

# Database Configuration
# NOTE: Update these with your actual MySQL credentials
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Kiranrani@1") 
DB_NAME = "ecommerce_db"

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
EMAIL_SENDER = "abhishekjindal724@gmail.com"
EMAIL_PASSWORD = "phys eorb vaed pdrn"
