# Web Scraper Learning Guide

Welcome! this guide is designed to help you understand every part of the "AI-Ready E-commerce Intelligence Tool" we are building.

## 1. The Technology Stack

### **Python**
The programming language used. It's popular for scraping because of its powerful libraries.

### **Selenium** (The Browser Automator)
- **What it does:** It acts like a robot user. It opens a real browser window (like Chrome), clicks buttons, scrolls, and types text.
- **Why we use it:** Many modern sites (Amazon, Flipkart) use JavaScript to load data. Traditional scrapers (like just `requests`) can't see this data because they don't run JavaScript. Selenium does.
- **Key Concept:** `driver.find_element(By.ID, "price")` tells the robot "Look for the HTML tag with `id='price'`".

### **BeautifulSoup** (The HTML Parser)
- **What it does:** Once Selenium loads the page, `BeautifulSoup` takes the raw HTML code and makes it easy to search.
- **Why we use it:** Selenium is great for *actions* (clicking), but BeautifulSoup is faster and easier for *reading* specific text from complex HTML structures.

### **Pandas** (The Data Organizer)
- **What it does:** Think of it as "Excel for Python". It holds data in tables called "DataFrames".
- **Why we use it:** It has powerful tools to clean data (e.g., removing "$" signs from prices, handling missing values) before we save it.

### **MySQL** (The Database)
- **What it does:** Stores data permanently in structured tables.
- **Why we use it:** Unlike a CSV file, a database allows multiple users/scripts to access data safely, handles millions of records efficiently, and allows complex queries (e.g., "Give me all products cheaper than $50").

---

## 2. Project Architecture Explained

### `config/settings.py`
This is the "Control Panel". Instead of hardcoding values like database passwords or the website URL inside the logic code, we put them here. This makes the code secure and easy to update.

### `core/scraper.py` (The Worker)
This file contains the logic to:
1. Open the browser.
2. Go to the URL.
3. Wait for the product list to load.
4. Extract the text (Name, Price, etc.).
5. **Anti-Blocking:** It waits for random amounts of time (e.g., 2 to 5 seconds) between actions so the website doesn't think it's a bot attacking them.

### `core/database_manager.py` (The Librarian)
This file handles talking to the database. It knows how to:
1. `connect()`: Login to MySQL.
2. `create_tables()`: Create the empty sheets (tables) if they don't exist.
3. `insert_product()`: Add a new row for a scraped product.

### `core/analyzer.py` (The Analyst)
This file takes the raw text and "polishes" it.
- **Sentiment Analysis:** It looks at reviews (e.g., "This product is amazing!") and gives it a score (Positive). In our starter version, we might use a simple rule-based approach (counting positive words), but this is where you'd plug in OpenAI/ChatGPT later.

### `main.py` (The Boss)
This script manages the workflow:
1. "Librarian, get the database ready."
2. "Worker, go scrape this URL."
3. "Analyst, clean this data."
4. "Librarian, save this cleaned data."

---

## 3. How to Run It
1. **Install Requirements:** `pip install -r requirements.txt`
2. **Setup MySQL:** Create a database named `ecommerce_db`.
3. **Configure:** Edit `config/settings.py` with your database password.
4. **Run:** `python main.py`
