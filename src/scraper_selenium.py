"""
Selenium-based web scraping module for extracting laptop data from BestBuy Canada.

This module uses Selenium WebDriver to handle JavaScript-rendered content.
Updated for the NEW Best Buy Canada website structure (2025).
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep, time
from random import randint
from loguru import logger


class BestBuySeleniumScraper:
    """
    Selenium-based scraper for Best Buy Canada website.
    Handles JavaScript-rendered content using Chrome WebDriver.
    """
    
    def __init__(self, config, headless=True):
        """
        Initialize the Selenium scraper.
        
        Args:
            config (dict): Configuration dictionary
            headless (bool): Run browser in headless mode (no GUI)
        """
        self.config = config
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """
        Set up Chrome WebDriver with appropriate options.
        """
        logger.info("Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        
        # Headless mode
        if self.headless:
            chrome_options.add_argument('--headless=new')
            logger.info("Running in headless mode (no browser window)")
        
        # Performance and compatibility options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # User agent
        user_agent = self.config.get('user_agent', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.add_argument(f'user-agent={user_agent}')
        
        # Disable automation flags to avoid detection
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Try to use system ChromeDriver first, fallback to WebDriver Manager
            try:
                # Use system chromium-chromedriver
                service = Service('/usr/bin/chromedriver')
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e:
                logger.debug(f"System chromedriver not found, trying WebDriver Manager: {e}")
                # Fallback to WebDriver Manager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set page load timeout
            self.driver.set_page_load_timeout(self.config.get('timeout', 30))
            
            logger.success("Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
            return False
    
    def close_driver(self):
        """
        Close the WebDriver and clean up.
        """
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver closed successfully")
            except Exception as e:
                logger.warning(f"Error closing WebDriver: {str(e)}")
    
    def wait_for_products(self, timeout=10):
        """
        Wait for product containers to load on the page.
        
        Args:
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if products loaded, False otherwise
        """
        try:
            # Wait for product containers with Schema.org markup
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[itemtype="http://schema.org/Product"]')
                )
            )
            logger.debug("Products loaded successfully")
            return True
            
        except TimeoutException:
            logger.warning(f"Timeout waiting for products to load (waited {timeout}s)")
            return False
    
    def scroll_page(self):
        """
        Scroll the page to load lazy-loaded content.
        """
        try:
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)  # Wait for lazy-loaded content
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            sleep(1)
            
        except Exception as e:
            logger.debug(f"Error scrolling page: {str(e)}")
    
    def scrape_page(self, url, request_num, start_time):
        """
        Scrape a single page using Selenium.
        
        Args:
            url (str): URL to scrape
            request_num (int): Current request number
            start_time (float): Start time of scraping session
            
        Returns:
            list: List of BeautifulSoup product containers
        """
        try:
            # Load the page
            logger.info(f'Request #{request_num} | Loading: {url[:80]}...')
            self.driver.get(url)
            
            # Wait for products to load
            if not self.wait_for_products(timeout=15):
                logger.warning("No products found or timeout")
                return None
            
            # Scroll to load lazy content
            self.scroll_page()
            
            # Get page source and parse with BeautifulSoup
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find product containers (note: HTML attributes are lowercase)
            containers = soup.find_all('div', {'itemtype': lambda x: x and 'Product' in x})
            
            # Monitor progress
            elapsed_time = time() - start_time
            logger.info(f'Request #{request_num} | Found {len(containers)} products | '
                       f'Frequency: {request_num/elapsed_time:.2f} req/s')
            
            return containers
            
        except Exception as e:
            logger.error(f'Request #{request_num} | Error: {str(e)}')
            return None
    
    def extract_laptop_data(self, container):
        """
        Extract data from a product container.
        
        Args:
            container: BeautifulSoup container element
            
        Returns:
            dict: Product data or None if extraction fails
        """
        try:
            # Extract product name
            name_h3 = container.find('h3', class_='productItemName_3IZ3c')
            if not name_h3:
                return None
            name = name_h3.get_text(strip=True)
            
            # Extract price
            price_span = container.find('span', class_='style-module_screenReaderOnly__4QmbS')
            if not price_span:
                price_div = container.find('div', class_='style-module_price__ql4Q1')
                price = price_div.get_text(strip=True) if price_div else None
            else:
                price = price_span.get_text(strip=True)
            
            if not price:
                return None
            
            # Extract rating and reviews
            rating = 0
            reviews = 0
            
            rating_container = container.find('span', class_='style-module_reviewCountContainer__HQlM5')
            if rating_container:
                rating_meta = rating_container.find('meta', {'itemprop': 'ratingValue'})
                review_meta = rating_container.find('meta', {'itemprop': 'reviewCount'})
                
                if rating_meta:
                    rating = float(rating_meta.get('content', 0))
                if review_meta:
                    reviews = int(review_meta.get('content', 0))
            
            return {
                'name': name,
                'price': price,
                'rating': rating,
                'reviews': reviews
            }
            
        except Exception as e:
            logger.debug(f"Error extracting product data: {str(e)}")
            return None
    
    def scrape_all_laptops(self, build_url_func):
        """
        Main scraping function - scrapes all pages based on configuration.
        
        Args:
            build_url_func: Function to build URLs
            
        Returns:
            dict: Dictionary containing lists of names, prices, ratings, and reviews
        """
        # Initialize data storage
        names, prices, ratings, reviews = [], [], [], []
        start_time = time()
        requests = 0
        successful_extractions = 0
        
        # Setup driver
        if not self.setup_driver():
            logger.error("Failed to initialize WebDriver. Aborting.")
            return {
                'names': names,
                'prices': prices,
                'ratings': ratings,
                'reviews': reviews
            }
        
        try:
            logger.info("=" * 60)
            logger.info("Starting Best Buy Canada laptop scraping with Selenium...")
            logger.info(f"Pages to scrape: {len(self.config['pages'])}")
            logger.info(f"RAM sizes to filter: {self.config['ram_sizes']}")
            logger.info("=" * 60)
            
            for ram_size in self.config['ram_sizes']:
                logger.info(f"\n--- Scraping RAM size: {ram_size}GB ---")
                
                for page in self.config['pages']:
                    # Random delay between requests
                    if requests > 0:
                        sleep_time = randint(
                            self.config['sleep_min'],
                            self.config['sleep_max']
                        )
                        logger.info(f"Sleeping for {sleep_time} seconds...")
                        sleep(sleep_time)
                    
                    requests += 1
                    
                    # Build URL and scrape
                    url = build_url_func(page, ram_size)
                    containers = self.scrape_page(url, requests, start_time)
                    
                    if not containers:
                        logger.warning(f"No data for RAM={ram_size}GB, Page={page}")
                        continue
                    
                    # Extract data from each product
                    page_extractions = 0
                    for container in containers:
                        data = self.extract_laptop_data(container)
                        
                        if data:
                            names.append(data['name'])
                            prices.append(data['price'])
                            ratings.append(data['rating'])
                            reviews.append(data['reviews'])
                            successful_extractions += 1
                            page_extractions += 1
                    
                    logger.info(f"✓ Extracted {page_extractions} laptops from this page")
                    
                    # Check max requests limit
                    if requests >= self.config['max_requests']:
                        logger.warning(f'Reached max requests ({self.config["max_requests"]})')
                        break
                
                if requests >= self.config['max_requests']:
                    break
            
            # Summary
            total_time = time() - start_time
            logger.info("\n" + "=" * 60)
            logger.info("SCRAPING COMPLETED!")
            logger.info(f"Total requests: {requests}")
            logger.info(f"Total laptops extracted: {successful_extractions}")
            logger.info(f"Total time: {total_time:.2f} seconds")
            logger.info(f"Average time per request: {total_time/requests:.2f} seconds")
            logger.info("=" * 60)
            
        finally:
            # Always close the driver
            self.close_driver()
        
        return {
            'names': names,
            'prices': prices,
            'ratings': ratings,
            'reviews': reviews
        }


def scrape_all_laptops(config, build_url_func):
    """
    Wrapper function to maintain compatibility with original interface.
    
    Args:
        config (dict): Configuration dictionary
        build_url_func: Function to build URLs
        
    Returns:
        dict: Dictionary containing lists of names, prices, ratings, and reviews
    """
    scraper = BestBuySeleniumScraper(config, headless=True)
    return scraper.scrape_all_laptops(build_url_func)
