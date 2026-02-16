import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config.settings import USER_AGENTS, DELAY_RANGE, HEADLESS

class EcomScraper:
    def __init__(self):
        self.driver = self._init_driver()

    def _init_driver(self):
        """Initializes the Selenium WebDriver with anti-blocking options."""
        options = Options()
        
        # Check if running on Linux (likely Streamlit Cloud)
        import platform
        if platform.system() == "Linux":
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--lang=en-US")
            
            # On Streamlit Cloud/Linux, chromium and chromium-driver are installed via packages.txt
            # We don't need webdriver_manager here, as it conflicts with the system driver.
            return webdriver.Chrome(options=options)
            
        elif HEADLESS:
            options.add_argument("--headless")
        
        # Random User-Agent
        user_agent = random.choice(USER_AGENTS)
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--lang=en-US") # Add language header
        
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        # Suppress logs
        options.add_argument("--log-level=3")

        # Use webdriver_manager to automatically handle the driver executable regarding usage on Windows/Mac
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def scrape_product(self, url):
        """Scrapes product details from a given URL."""
        try:
            self.driver.get(url)
            self._random_delay()
            
            # Simple scroll to trigger lazy loading
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # --- TITLE EXTRACTION ---
            data = self._parse_html(soup)
            data["reviews"] = self._scrape_reviews(soup)
            return data
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

    def _parse_html(self, soup):
        """
        Parses the HTML and extracts product info.
        Optimized for Amazon but compatible with generic structures.
        """
        title = "Unknown Product"
        price = "N/A"
        availability = "Unknown"
        rating = "N/A"
        
        # 1. Title
        title_tag = soup.select_one("#productTitle")
        if not title_tag:
            # Fallback to h1, but avoid common non-title h1s like the 'pqv-ingress' (Product summary tooltip)
            title_tag = soup.select_one("h1:not(#pqv-ingress)")
            
        if title_tag:
            # Remove hidden text often found in Amazon titles (accessibility, UI hints)
            for hidden in title_tag.select(".a-offscreen, .screen-reader-text, .visually-hidden"):
                hidden.decompose()
            title = title_tag.get_text(strip=True)
            
        # 2. Price (Amazon specific complex logic)
        # Try finding the 'offscreen' price which is hidden but contains the correct value
        price_tag = soup.select_one(".a-price .a-offscreen, #priceblock_ourprice, #priceblock_dealprice, .price")
        if price_tag:
            price = price_tag.text.strip()
        else:
             # Fallback
             text_price = soup.find(string=lambda t: t and ("$" in t or "€" in t or "£" in t))
             if text_price:
                 price = text_price.strip()

        # 3. Availability
        avail_tag = soup.select_one("#availability, .availability")
        if avail_tag:
            availability = avail_tag.text.strip()

        # 4. Rating
        rating_tag = soup.select_one("i.a-icon-star span, .a-icon-alt")
        if rating_tag:
            rating = rating_tag.text.strip()
            
        return {
            "name": title,
            "price": price,
            "availability": availability,
            "rating": rating,
            "raw_html_len": len(str(soup))
        }

    def _scrape_reviews(self, soup):
        """Extracts text reviews from the product page."""
        reviews = []
        try:
            # Scroll down to load reviews (dynamic loading)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1) # Wait for potential lazy load
            
            # Update soup after scroll
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # Amazon review text selectors
            review_elements = soup.select('div[data-hook="review-collapsed"]')
            
            if not review_elements:
                 # Try alternative selector
                 review_elements = soup.select('span[data-hook="review-body"] span')

            for el in review_elements[:10]: # Limit to 10 reviews
                text = el.get_text().strip()
                if text:
                    reviews.append(text)
            
            print(f"Scraped {len(reviews)} reviews.")
        except Exception as e:
            print(f"Error scraping reviews: {e}")
        
        return reviews

    def _random_delay(self):
        """Waits for a random amount of time to simulate human behavior."""
        sleep_time = random.uniform(*DELAY_RANGE)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

    def close(self):
        """Closes the browser."""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")
