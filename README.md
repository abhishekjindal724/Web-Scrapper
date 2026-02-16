# 🛒 AI-Ready E-commerce Intelligence Tool

> **A professional-grade web scraper and price monitoring solution built for the Cloud.**
> *Deployed on Streamlit Cloud • Persistent Data with TiDB • Automated via GitHub Actions*

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)
![Database](https://img.shields.io/badge/Database-TiDB%20(MySQL)-orange.svg)
![Automation](https://img.shields.io/badge/Automation-GitHub%20Actions-black.svg)

## 🚀 Overview

This application is not just a scraper; it's a **full-stack intelligence tool** designed to track e-commerce product prices, analyze sentiment from reviews, and automate price drop alerts.

Unlike typical scripts that run locally, this project is **Cloud-Native**. It runs 24/7 without a laptop, leveraging serverless architecture to scrape, store, and notify.

### ✨ Key Features

*   **🕵️‍♂️ Advanced Scraping**: Uses `Selenium` with Headless Chrome to bypass anti-bot protections (User-Agent rotation, lazy loading handling).
*   **📊 Real-Time Dashboard**: Interactive UI built with Streamlit to visualize product data, ratings, and sentiment scores.
*   **🧠 Sentiment Analysis**: Uses NLP (`TextBlob`) to analyze customer reviews and determine if a product is worth buying (Positive/Neutral/Negative).
*   **💾 Persistent Cloud Storage**: Integrates with **TiDB Serverless** (MySQL) to store alerts and product history securely via SSL.
*   **🤖 Automated Monitoring**: A background "Robot" (GitHub Actions Cron Job) wakes up every 6 hours to check prices and send alerts.
*   **📧 Smart Notifications**: Sends email alerts via SMTP only when a price drop target is met.

---

## 🏗️ Architecture

1.  **Frontend**: Streamlit App (hosted on Streamlit Community Cloud).
2.  **Engine**: Python + Selenium + BeautifulSoup4.
3.  **Database**: TiDB Serverless (MySQL).
4.  **DevOps**: GitHub Actions (Scheduled Workflows).

---

## 🛠️ Installation & Setup

### 1. Local Development
```bash
# Clone the repo
git clone https://github.com/yourusername/Web-Scrapper.git
cd Web-Scrapper

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run dashboard.py
```

### 2. Secrets Management
Create a `.streamlit/secrets.toml` file for local keys:
```toml
[default]
DB_HOST = "gateway01.us-west-2.prod.aws.tidbcloud.com"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_NAME = "test"
EMAIL_PASSWORD = "your_app_password"
```

---

## 🧠 How it Works (Under the Hood)

THIS IS A CLOUD-NATIVE APPLICATION.

1.  **Frontend (Streamlit)**:
    - Hosted on **Streamlit Community Cloud**.
    - Handles user interactions (URL input, setting alerts).
    - *Auto-Deployment*: Pushing to GitHub automatically updates the live app.

2.  **Scraper (Selenium)**:
    - Runs in **Headless Mode** (invisible Chrome browser).
    - Rotates User-Agents to bypass anti-bot protections.
    - Extracts Price, Rating, Availability, and Reviews.

3.  **Brain (TiDB Serverless)**:
    - A persistent **MySQL** database in the cloud.
    - Stores your configured alerts securely (using SSL).
    - Ensures data survives even when the app restarts.

4.  **Robot (GitHub Actions)**:
    - A **Cron Job** that wakes up every 6 hours.
    - Runs `check_alerts.py` on a separate Ubuntu server.
    - Checks if `Current Price <= Target Price`.
    - Sends an email via Gmail SMTP if a deal is found.

5.  **Intelligence (NLP)**:
    - Uses `TextBlob` to analyze review sentiment.
    - Gives a "Vibe Check" score (-1.0 to 1.0) on whether people like the product.

## 🧪 Testing the Automation

You don't need to wait 6 hours to test!
1.  Go to **GitHub Actions** tab in your repo.
2.  Select **Price Monitor** workflow.
3.  Click **Run workflow**.
    - *Green Checkmark ✅* = System is healthy.
    - *Email Received 📧* = Deal found!

---

## 📸 Screenshots

*(Add your dashboard screenshots here)*

---

## 📝 License
MIT License. Free to use for educational and portfolio purposes.
