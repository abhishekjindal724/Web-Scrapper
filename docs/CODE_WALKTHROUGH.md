# Project Code Walkthrough (Simple English)

This guide explains what every single file in the project does, using simple analogies.

---

## 1. The "Command Center"
### `main.py`
- **What it is:** The main boss script.
- **What it does:** It tells everyone else what to do. It says "Go to these websites, get the data, analyze it, and save it." You run this if you want to scrape a list of URLs all at once.

### `dashboard.py` (The Remote Control)
- **What it is:** The visual screen you see in your browser.
- **What it does:** It lets you paste a link and press a button to scrape *one* product instantly. It shows you the price, rating, and reviews nicely. It also lets you set price alerts.

### `check_alerts.py` (The Security Guard)
- **What it is:** A robot that watches prices for you.
- **What it does:** It runs in the background. Every hour, it checks the list of alerts you set. If a price drops below your target, it screams (sends an email).

---

## 2. The "Worker Bots" (Core Folder)
### `core/scraper.py` (The Shopper)
- **What it is:** A robot that visits Amazon.
- **What it does:** It opens a hidden browser (Chrome), goes to the product page, and writes down the Title, Price, and Reviews. It tries to act like a human so it doesn't get blocked.

### `core/analyzer.py` (The Brain)
- **What it is:** The data analyst.
- **What it does:** It takes the messy text (like "$1,299.00") and cleans it (to number `1299.00`). It also reads the reviews and decides if people are happy (Positive) or angry (Negative).

### `core/database_manager.py` (The File Cabinet)
- **What it is:** The librarian.
- **What it does:** It handles saving everything to the MySQL database. It knows how to Create Tables, Save Products, and Read Alerts. It makes sure we don't lose data.

### `core/notifier.py` (The Postman)
- **What it is:** The email sender.
- **What it does:** It takes a message ("Price Drop!") and sends it to your email using Gmail's servers.

---

## 3. The "Rule Book" (Config Folder)
### `config/settings.py`
- **What it is:** The settings file.
- **What it does:** It stores secrets like your Database Password and Email Password. It also sets rules, like "Wait 2-5 seconds between clicks".

---

## 4. Other Files
- `requirements.txt`: A shopping list for Python. It tells your computer which tools (libraries) to install.
- `docs/LEARNING_GUIDE.md`: A textbook explaining the project.
- `TESTING_GUIDE.md`: A checklist to make sure everything works.
