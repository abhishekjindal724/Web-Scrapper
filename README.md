<div align="center">

# 🚀 E-com Intel Pro

### AI-Powered E-commerce Intelligence & Price Monitoring

**Live scraping • Sentiment analysis • Automated price alerts • Cloud-native**

[![Live Demo](https://img.shields.io/badge/🔗_Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge)](https://abhishekjindal724s-apps.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Selenium](https://img.shields.io/badge/Selenium-Headless_Chrome-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://selenium.dev)
[![TiDB](https://img.shields.io/badge/Database-TiDB_Serverless-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://tidbcloud.com)
[![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

</div>

---

## ⚡ What is This?

**E-com Intel Pro** is a full-stack, cloud-native tool that scrapes Amazon product data in real-time, analyzes customer sentiment using NLP, and sends automated price drop alerts via email — all running 24/7 without a laptop.

> **This is NOT just a scraper.** It's a complete intelligence pipeline:  
> `Scrape → Analyze → Store → Monitor → Alert`

---

## 🎯 Key Features

| Feature | Description |
|---|---|
| 🕵️ **Stealth Scraping** | Selenium + Headless Chrome with anti-bot evasion (User-Agent rotation, automation flag masking) |
| 📊 **Live Dashboard** | Premium glassmorphism UI with real-time product cards, ratings, and visual sentiment gauge |
| 🧠 **NLP Sentiment** | TextBlob-powered review analysis — determines if a product is loved, hated, or meh |
| 💰 **Price Alerts** | Set a target price → get an email when it drops. Powered by GitHub Actions cron |
| ☁️ **Cloud-Native** | Deployed on Streamlit Cloud + TiDB Serverless + GitHub Actions. Zero infrastructure to manage |
| 📧 **Smart Notifications** | Gmail SMTP alerts with product details and direct purchase links |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER                                     │
│                    Enters Amazon URL                             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  📊 STREAMLIT DASHBOARD (Streamlit Community Cloud)              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │ Price Card  │  │ Rating     │  │ Sentiment  │  │ Reviews   │ │
│  │ ₹2,499     │  │ ⭐ 4.2     │  │ 😊 78%     │  │ Top 5     │ │
│  └────────────┘  └────────────┘  └────────────┘  └───────────┘ │
└──────────────────────┬──────────────────────────────────────────┘
                       │
           ┌───────────┼───────────┐
           ▼           ▼           ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ 🕵️ Scraper│  │ 🧠 NLP    │  │ 💾 TiDB  │
   │ Selenium  │  │ TextBlob  │  │ MySQL    │
   │ + BS4     │  │ Sentiment │  │ (Cloud)  │
   └──────────┘  └──────────┘  └────┬─────┘
                                    │
                                    ▼
                          ┌──────────────────┐
                          │ 🤖 GitHub Actions │
                          │ Cron: Every 6hrs  │
                          │ check_alerts.py   │
                          └────────┬─────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │ 📧 Email Alert    │
                          │ Gmail SMTP        │
                          │ "Price dropped!"  │
                          └──────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit | Interactive dashboard with custom CSS |
| **Scraping** | Selenium + BeautifulSoup4 | Headless Chrome browser automation |
| **NLP** | TextBlob | Review sentiment analysis |
| **Database** | TiDB Serverless (MySQL) | Persistent cloud storage with SSL |
| **Automation** | GitHub Actions | Cron-based price monitoring every 6h |
| **Email** | Gmail SMTP | Price drop notifications |
| **Deployment** | Streamlit Cloud | Auto-deploy on git push |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/abhishekjindal724/Web-Scrapper.git
cd Web-Scrapper
pip install -r requirements.txt
```

### 2. Configure Secrets

Create `.streamlit/secrets.toml`:

```toml
DB_HOST = "your-tidb-host.tidbcloud.com"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_NAME = "test"
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_gmail_app_password"
```

> 💡 **Tip:** For `EMAIL_PASSWORD`, use a [Gmail App Password](https://myaccount.google.com/apppasswords), not your regular password.

### 3. Run Locally

```bash
streamlit run dashboard.py
```

---

## 📁 Project Structure

```
Web-Scrapper/
├── dashboard.py            # Streamlit UI — premium glassmorphism design
├── check_alerts.py         # Alert checker (runs via GitHub Actions)
├── style.css               # Custom CSS theme
├── main.py                 # CLI entry point
│
├── core/
│   ├── scraper.py          # Selenium scraper with anti-bot evasion
│   ├── analyzer.py         # TextBlob sentiment analysis engine
│   ├── database_manager.py # TiDB/MySQL + SQLite fallback
│   └── notifier.py         # Gmail SMTP email sender
│
├── config/
│   └── settings.py         # Environment-aware config loader
│
├── .github/workflows/
│   └── price_monitor.yml   # GitHub Actions cron job (every 6h)
│
├── packages.txt            # System dependencies (Chromium)
├── requirements.txt        # Python dependencies
└── runtime.txt             # Python version for Streamlit Cloud
```

---

## 🤖 How the Alert System Works

```
You set alert: "Notify me when iPhone drops below ₹50,000"
                              │
                              ▼
              ┌───────────────────────────────┐
              │  Alert saved to TiDB Database  │
              └───────────────┬───────────────┘
                              │
            Every 6 hours (GitHub Actions cron)
                              │
                              ▼
              ┌───────────────────────────────┐
              │  check_alerts.py runs          │
              │  → Fetches pending alerts      │
              │  → Scrapes current price       │
              │  → Compares: current ≤ target? │
              └───────────────┬───────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                YES ▼                   ▼ NO
          ┌──────────────┐     ┌──────────────┐
          │ 📧 Send Email │     │ ⏳ Check again │
          │ Mark as sent  │     │ in 6 hours    │
          └──────────────┘     └──────────────┘
```

### Test It Yourself

1. Go to **GitHub → Actions** tab → **Price Monitor**
2. Click **Run workflow** → triggers immediately
3. ✅ Green = System healthy
4. 📧 Check inbox for the alert email

---

## 🧠 Sentiment Analysis

The NLP engine analyzes Amazon reviews and outputs:

| Score Range | Verdict | Emoji |
|---|---|---|
| 0.7 → 1.0 | **Very Positive** | 😍 |
| 0.3 → 0.7 | **Positive** | 😊 |
| -0.3 → 0.3 | **Neutral / Mixed** | 😐 |
| -0.7 → -0.3 | **Negative** | 😟 |
| -1.0 → -0.7 | **Very Negative** | 😡 |

The dashboard displays this as a **visual gradient gauge bar** (red → yellow → green) with a marker showing exactly where the product lands.

---

## 🛡️ Anti-Bot Measures

| Technique | Implementation |
|---|---|
| User-Agent Rotation | Random browser UA per session |
| Automation Masking | `--disable-blink-features=AutomationControlled` |
| Lazy Load Handling | Scroll simulation to trigger dynamic content |
| Rate Limiting | Random delays (2-5s) between requests |
| Headless Chrome | Full browser rendering for JS-heavy pages |

---

## ☁️ Deployment

### Streamlit Cloud (Dashboard)
- Auto-deploys on `git push` to `main`
- Secrets managed via Streamlit Cloud dashboard
- System deps via `packages.txt` (Chromium)

### GitHub Actions (Price Monitor)
- Cron schedule: `0 0,6,12,18 * * *` (every 6 hours UTC)
- Secrets: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `EMAIL_SENDER`, `EMAIL_PASSWORD`
- Manual trigger available via `workflow_dispatch`

---

## 🗺️ Roadmap

- [ ] Multi-platform support (Flipkart, Myntra)
- [ ] Price history graphs with trend analysis
- [ ] WhatsApp/Telegram alert channels
- [ ] Product comparison mode
- [ ] AI-powered purchase recommendations

---

## 📄 License

MIT License — free to use for educational and portfolio purposes.

---

<div align="center">

**Built with ❤️ by [Abhishek Jindal](https://github.com/abhishekjindal724)**

*If this helped you, drop a ⭐ on the repo!*

</div>
