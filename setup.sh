#!/bin/bash

# Update package list
sudo apt-get update

# Install Python 3 and pip
sudo apt-get install -y python3 python3-pip

# Install Chrome (for Selenium)
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Install project dependencies
pip3 install -r requirements.txt

# Create systemd service for background execution
# (Optional: Customize user and path as needed)
# sudo nano /etc/systemd/system/scraper.service

echo "Setup complete! You can now run the scraper."
