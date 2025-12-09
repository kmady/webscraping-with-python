"""
Web scraping module for extracting laptop data from BestBuy Canada.

Updated for the NEW Best Buy Canada website structure (2025).
The website is now React-based with different HTML structure.
"""

from requests import get
from bs4 import BeautifulSoup
from time import sleep, time
from random import randint
from loguru import logger
import re


def extract_rating_and_reviews(container):
    """
    Extracts rating and review count from a laptop container.
    
    Args:
        container: BeautifulSoup container element
    
    Returns:
        tuple: (rating_value, review_count) or (None, None) if not found
    """
    try:
        # Look for aggregateRating schema
        rating_div = container.find('span', class_='style-module_reviewCountContainer__HQlM5')
        if rating_div:
            # Extract rating value from meta tag
            rating_meta = rating_div.find('meta', {'itemprop': 'ratingValue'})
            review_meta = rating_div.find('meta', {'itemprop': 'reviewCount'})
            
            if rating_meta and review_meta:
                rating = float(rating_meta.get('content', 0))
                reviews = int(review_meta.get('content', 0))
                return rating, reviews
    except Exception as e:
        logger.debug(f"Error extracting rating: {str(e)}")
    
    return None, None


def extract_price(container):
    """
    Extracts price from a laptop container.
    
    Args:
        container: BeautifulSoup container element
    
    Returns:
        str: Price string or None if not found
    """
    try:
        # Look for the price in the screen reader text (most reliable)
        price_span = container.find('span', class_='style-module_screenReaderOnly__4QmbS')
        if price_span:
            price_text = price_span.get_text(strip=True)
            return price_text
        
        # Fallback: try the visible price div
        price_div = container.find('div', class_='style-module_price__ql4Q1')
        if price_div:
            price_text = price_div.get_text(strip=True)
            return price_text
            
    except Exception as e:
        logger.debug(f"Error extracting price: {str(e)}")
    
    return None


def extract_laptop_data(container):
    """
    Extracts all relevant data from a laptop container.
    
    Args:
        container: BeautifulSoup container element
    
    Returns:
        dict: Dictionary containing name, price, rating, and reviews
              Returns None if essential data is missing
    """
    try:
        # Extract product name
        name_h3 = container.find('h3', class_='productItemName_3IZ3c')
        if not name_h3:
            logger.debug("No product name found, skipping")
            return None
        
        name = name_h3.get_text(strip=True)
        
        # Extract price
        price = extract_price(container)
        if not price:
            logger.debug(f"No price found for {name}, skipping")
            return None
        
        # Extract rating and reviews
        rating, reviews = extract_rating_and_reviews(container)
        
        return {
            'name': name,
            'price': price,
            'rating': rating if rating is not None else 0,
            'reviews': reviews if reviews is not None else 0
        }
    except Exception as e:
        logger.error(f"Error extracting laptop data: {str(e)}")
        return None


def scrape_page(url, request_num, start_time, config):
    """
    Scrapes a single page and returns laptop containers.
    
    Args:
        url (str): URL to scrape
        request_num (int): Current request number
        start_time (float): Start time of scraping session
        config (dict): Configuration dictionary
    
    Returns:
        list: List of laptop containers or None if error
    """
    # Get headers from config or use default
    user_agent = config.get('user_agent', 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        # Make request with headers and timeout
        timeout = config.get('timeout', 30)
        response = get(url, headers=headers, timeout=timeout)
        
        # Monitor requests
        elapsed_time = time() - start_time
        logger.info(f'Request #{request_num} | Frequency: {request_num/elapsed_time:.2f} req/s | URL: {url[:80]}...')
        
        # Check status code
        if response.status_code != 200:
            logger.warning(f'Request #{request_num} | Status code: {response.status_code}')
            return None
        
        # Parse HTML
        page_html = BeautifulSoup(response.text, 'html.parser')
        
        # Find product containers - NEW STRUCTURE
        # Products are in <div> with class containing "listItem" and itemType schema
        containers = page_html.find_all('div', {'itemType': 'http://schema.org/Product'})
        
        if not containers:
            logger.warning(f'No product containers found on page. HTML might be dynamically loaded.')
            logger.debug(f'Page title: {page_html.title.string if page_html.title else "No title"}')
            # Try alternative selector
            containers = page_html.find_all('div', class_=lambda x: x and 'listItem' in x)
        
        logger.info(f'Found {len(containers)} product containers on page')
        return containers
        
    except Exception as e:
        logger.error(f'Request #{request_num} | Error: {str(e)}')
        return None


def scrape_all_laptops(config, build_url_func):
    """
    Scrapes all laptop data based on configuration.
    
    Args:
        config (dict): Configuration dictionary
        build_url_func (function): Function to build URLs
    
    Returns:
        dict: Dictionary containing lists of names, prices, ratings, and reviews
    """
    names, prices, ratings, reviews = [], [], [], []
    start_time = time()
    requests = 0
    successful_extractions = 0
    
    logger.info("=" * 60)
    logger.info("Starting Best Buy Canada laptop scraping...")
    logger.info(f"Pages to scrape: {len(config['pages'])}")
    logger.info(f"RAM sizes to filter: {config['ram_sizes']}")
    logger.info("=" * 60)
    
    for ram_size in config['ram_sizes']:
        logger.info(f"\n--- Scraping RAM size: {ram_size}GB ---")
        
        for page in config['pages']:
            # Random delay between requests to be respectful
            if requests > 0:  # Don't sleep before first request
                sleep_time = randint(config['sleep_min'], config['sleep_max'])
                logger.info(f"Sleeping for {sleep_time} seconds...")
                sleep(sleep_time)
            
            requests += 1
            
            # Build and scrape URL
            url = build_url_func(page, ram_size)
            containers = scrape_page(url, requests, start_time, config)
            
            if containers is None or len(containers) == 0:
                logger.warning(f"No data found for RAM={ram_size}GB, Page={page}")
                continue
            
            # Extract data from containers
            page_extractions = 0
            for container in containers:
                data = extract_laptop_data(container)
                
                if data:
                    names.append(data['name'])
                    prices.append(data['price'])
                    ratings.append(data['rating'])
                    reviews.append(data['reviews'])
                    successful_extractions += 1
                    page_extractions += 1
            
            logger.info(f"Extracted {page_extractions} laptops from this page")
            
            # Check if max requests exceeded
            if requests >= config['max_requests']:
                logger.warning(f'Reached maximum requests limit ({config["max_requests"]}). Stopping.')
                break
        
        if requests >= config['max_requests']:
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
    
    return {
        'names': names,
        'prices': prices,
        'ratings': ratings,
        'reviews': reviews
    }
