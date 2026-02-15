# Testing Guide: AI-Ready E-commerce Intelligence Tool

Follow these steps to test the entire system from start to finish.

## Prerequisites
1.  **Dependencies Installed**: Ensure you ran `pip install -r requirements.txt`.
2.  **Database Configured**: Ensure MySQL is running.
3.  **Fresh Start (Optional)**: If you want to test from scratch, truncate the `products` and `alerts` tables in MySQL.

---

## Step 1: Start the Monitor (Background)
Open a terminal and run:
```bash
python check_alerts.py
```
*Note: Currently set to check every **1 minute** for testing.*

## Step 2: Start the Dashboard
Open a **new** terminal and run:
```bash
python -m streamlit run dashboard.py
```
This will open the web interface in your browser.

## Step 2: Scrape a Product
1.  Find an Amazon product URL (e.g., a book or electronic item).
2.  Paste it into the dashboard's **Product URL** field.
3.  Click **Scrape & Analyze**.
4.  **Verify**:
    - Product Name, Price, and Rating appear.
    - Sentiment Score is calculated.
    - Reviews are listed in the expander.

## Step 3: Set a Price Alert (Test Mode)
1.  In the Dashboard, scroll down to **"Set Price Alert"**.
2.  Enter a **Target Price** that is **HIGHER** than the current price (e.g., if current is ₹500, enter ₹1000).
    - *Why?* This ensures the alert condition (Current <= Target) is met immediately for testing.
3.  Enter your **Email Address**.
4.  Click **Set Alert**. You should see a success message.

## Step 4: Verify Automation
1.  Check the terminal running `check_alerts.py`.
2.  It should print:
    - `Checking alerts...`
    - `checking [URL]...`
    - `📉 Price Drop Detected!`
    - `Email sent successfully.`

## Step 5: Check Email
1.  Check your inbox for the alert.

## Step 6: Verify Automation
1.  Leave `check_alerts.py` running.
2.  It will print "Sleeping for 1 hour...".
3.  This confirms the background monitor is active.

---

**Troubleshooting:**
- **No Email?** Check `config/settings.py` credentials. Google App Passwords are required.
- **Database Error?** Ensure XAMPP/MySQL is running.
- **Scraper Blocked?** Try a different product URL or check your internet connection.
