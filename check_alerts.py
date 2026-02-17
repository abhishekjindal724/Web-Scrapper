import time
import sys
import io
from core.database_manager import DatabaseManager
from core.scraper import EcomScraper
from core.notifier import EmailNotifier
from config.settings import EMAIL_SENDER, EMAIL_PASSWORD

def check_alerts_once():
    """Performs a single pass of price checks for all pending alerts."""
    processed_count = 0
    try:
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Checking alerts...")
        db = DatabaseManager()
        if not db.connect():
            print("Failed to connect to DB.")
            return 0
        
        # Ensure tables exist (just in case)
        db.create_tables()

        # Initialize Notifier
        notifier = EmailNotifier(EMAIL_SENDER, EMAIL_PASSWORD)

        alerts = db.get_pending_alerts()
        if not alerts:
            print("No pending alerts found.")
            db.close()
            return 0
            
        print(f"Checking {len(alerts)} items...")
        scraper = EcomScraper()
        
        for alert in alerts:
            alert_id, url, target_price, recipient_email = alert
            
            try:
                data = scraper.scrape_product(url)
                if not data:
                    continue
                    
                # Use robust numeric price from scraper (handles ranges safely)
                current_price = data.get('price_numeric', 0.0)
                
                # Fallback for old scraper versions or failures
                if not current_price:
                    current_price_str = data.get('price', '0')
                    # cleanup price (remove currency symbols)
                    clean_price = "".join(c for c in current_price_str if c.isdigit() or c == '.')
                    try:
                        current_price = float(clean_price)
                    except:
                        current_price = 0.0

                product_name = data.get('name', 'Unknown Product')
                
                # Check condition (Price Drop)
                if current_price > 0 and current_price <= float(target_price):
                    print(f"📉 Price Drop: {current_price} <= Target: {target_price}")
                    
                    # Try to send email
                    if notifier.send_price_alert(recipient_email, product_name, current_price, float(target_price), url):
                        print(f"Email sent to {recipient_email}")
                        db.mark_alert_sent(alert_id)
                        processed_count += 1
                else:
                    print(f"Price {current_price} is still above target {target_price}")
                
            except Exception as e:
                print(f"Error checking alert {alert_id}: {e}")
                
            time.sleep(2) # Polite delay between checks

        scraper.close()
        db.close()
        return processed_count
        
    except Exception as e:
        print(f"Critical Error: {e}")
        return 0

def check_alerts():
    print("Starting Price Alert Monitor... (Press Ctrl+C to stop)", flush=True)
    
    while True:
        check_alerts_once()
        print("Sleeping for 6 hours...")
        time.sleep(21600)

if __name__ == "__main__":
    import sys
    try:
        if "--loop" in sys.argv:
            check_alerts()
        else:
            print("Running in single-pass mode (for Cron/GitHub Actions)...")
            count = check_alerts_once()
            print(f"Finished. Processed {count} alerts.")
    except KeyboardInterrupt:
        print("\nMonitor stopped.")


