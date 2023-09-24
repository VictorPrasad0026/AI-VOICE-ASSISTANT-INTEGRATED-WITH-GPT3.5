import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
url = "https://leetcode.com/rishabhvctor/"  # Replace with the website URL you want to scrape
response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.content, 'html.parser')

# Extract data from the website
# For example, find all <a> tags and print their text and URLs
for link in soup.find_all(''):
    link_text = link.text
    link_url = link.get('href')
    print(f"Link Text: {link_text}\nLink URL: {link_url}\n")
