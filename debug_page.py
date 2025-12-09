"""Debug script to inspect the actual HTML structure from Best Buy."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    url = 'https://www.bestbuy.ca/en-ca/category/windows-laptops/36711?page=1&path=category%3AComputers%2B%2526%2BTablets%3Bcategory%3ALaptops%2B%2526%2BMacBooks%3Bcategory%3AWindows%2BLaptops%3Bcustom0ramsize%3A8'
    
    print(f"Loading: {url}")
    driver.get(url)
    
    # Wait and scroll
    sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3)
    
    # Get page source
    html = driver.page_source
    
    # Save to file
    with open('/home/dem/workspace/webscraping-with-python/debug_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✓ Page source saved to debug_page.html")
    print(f"  Page title: {driver.title}")
    print(f"  HTML length: {len(html)} characters")
    
    # Try to find products with different selectors
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    print("\nTesting selectors:")
    print(f"  div[itemtype*='Product']: {len(soup.find_all('div', {'itemtype': lambda x: x and 'Product' in x}))}")
    print(f"  div[itemtype='http://schema.org/Product']: {len(soup.find_all('div', {'itemType': 'http://schema.org/Product'}))}")
    print(f"  h3 with 'productItem': {len(soup.find_all('h3', class_=lambda x: x and 'productItem' in x))}")
    print(f"  div with 'productItem': {len(soup.find_all('div', class_=lambda x: x and 'productItem' in x))}")
    print(f"  All divs: {len(soup.find_all('div'))}")
    
    # Show first few product-like divs
    product_divs = soup.find_all('div', class_=lambda x: x and ('product' in x.lower() or 'item' in x.lower()))[:5]
    print(f"\nFirst 5 product-like divs:")
    for i, div in enumerate(product_divs):
        classes = div.get('class', [])
        print(f"  {i+1}. Classes: {classes[:3] if len(classes) > 3 else classes}")
    
finally:
    driver.quit()
    print("\n✓ Browser closed")
