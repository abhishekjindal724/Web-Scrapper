import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import DB_USER # Using a placeholder, user should add EMAIL_USER/PASS to settings

# Placeholder config - User needs to add these to config/settings.py
# EMAIL_SENDER = "your_email@gmail.com"
# EMAIL_PASSWORD = "your_app_password"

class EmailNotifier:
    def __init__(self, sender_email=None, sender_password=None):
        self.sender_email = sender_email
        self.sender_password = sender_password
        
    def send_price_alert(self, recipient_email, product_name, current_price, target_price, url):
        if not self.sender_email or not self.sender_password:
            print("Email credentials not set. Skipping email.")
            return False

        subject = f"Price Drop Alert: {product_name[:30]}..."
        body = f"""
        Good news!
        
        The price for '{product_name}' has dropped to {current_price}.
        Your target was {target_price}.
        
        Grab it here: {url}
        """

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient_email, text)
            server.quit()
            print(f"Email sent to {recipient_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
