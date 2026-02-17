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
        
        # Random User-Agent (CRITICAL for anti-bot)
        user_agent = random.choice(USER_AGENTS)
        options.add_argument(f"user-agent={user_agent}")
        
        # Common anti-detection options for ALL platforms
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--lang=en-US,en;q=0.9")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Check if running on Linux (Streamlit Cloud / GitHub Actions)
        import platform
        if platform.system() == "Linux":
            options.add_argument("--headless=new")  # new headless mode, harder to detect
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=options)
        else:
            if HEADLESS:
                options.add_argument("--headless=new")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        
        # CDP stealth: override navigator.webdriver to return undefined
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = {runtime: {}};
            """
        })
        
        return driver

    def scrape_product(self, url):
        """Scrapes product details from a given URL."""
        try:
            self.driver.get(url)
            self._random_delay()
            
            # Wait for page to fully render (important on slow CI runners)
            time.sleep(3)
            
            # Scroll to trigger lazy loading
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # --- TITLE EXTRACTION ---
            data = self._parse_html(soup)
            
            # DEBUG: Capture screenshot if data is missing (Anti-Bot check)
            if data["name"] == "Unknown Product":
                print("Potential Bot Block detected. Taking screenshot...")
                screenshot = self.driver.get_screenshot_as_png()
                data["debug_screenshot"] = screenshot
            elif not data.get("price") or data.get("price") == "N/A":
                print("Price not found! Taking debug screenshot...")
                screenshot = self.driver.get_screenshot_as_png()
                data["debug_screenshot"] = screenshot
            
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
            
        # 2. Price — scoped to the MAIN price container (not variant thumbnails)
        price_str = "N/A"
        price_val = 0.0
        
        # Priority chain: most specific → broadest fallback
        price_selectors = [
            ".priceToPay .a-offscreen",                                       # Modern Amazon.in (variant pages)
            "#corePriceDisplay_desktop_feature_div .a-price .a-offscreen",    # New desktop layout
            "#corePrice_feature_div .a-price .a-offscreen",                   # Older desktop layout  
            "#tp_price_block_total_price_ww .a-offscreen",                    # Total price block
            "#price_inside_buybox",                                           # Buy box price
            "#newBuyBoxPrice",                                                # New buy box
            "#priceblock_ourprice",                                           # Legacy
            "#priceblock_dealprice",                                          # Legacy deal
            ".a-price .a-offscreen",                                          # Broadest fallback
        ]
        
        matched_selector = None
        for selector in price_selectors:
            tag = soup.select_one(selector)
            if tag:
                text = tag.get_text(strip=True)
                # Only accept if text is non-empty AND contains at least one digit
                if text and any(c.isdigit() for c in text):
                    price_str = text
                    matched_selector = selector
                    print(f"✅ Price found via: {selector} -> '{price_str}'")
                    break
                else:
                    print(f"⚠️ Selector '{selector}' matched but text was empty/invalid: '{text}'")
        
        if not matched_selector:
            # Last resort: search for ₹ symbol in any text node
            text_price = soup.find(string=lambda t: t and "₹" in t and any(c.isdigit() for c in t))
            if text_price:
                price_str = text_price.strip()
                print(f"✅ Price found via ₹ text search -> '{price_str}'")
            else:
                print("❌ WARNING: No price found with ANY selector!")
                # Try to dump what price-related elements exist on the page
                all_price_elements = soup.select(".a-price")
                print(f"   Found {len(all_price_elements)} .a-price elements on page")
                for i, el in enumerate(all_price_elements[:5]):
                    print(f"   .a-price[{i}]: '{el.get_text(strip=True)[:50]}'")

        # Parse numeric value from the price string
        try:
            clean_str = "".join(c for c in price_str if c.isdigit() or c == '.')
            price_val = float(clean_str) if clean_str else 0.0
        except:
            price_val = 0.0

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
            "price": price_str,
            "price_numeric": price_val, 
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
            time.sleep(1) 
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
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
