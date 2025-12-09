"""
Web scraping module for extracting laptop data from BestBuy.
"""

from requests import get
from bs4 import BeautifulSoup
from IPython.core.display import clear_output
from warnings import warn
from time import sleep, time
from random import randint


def extract_rating(container):
    """
    Extracts rating value from a laptop container.
    
    Args:
        container: BeautifulSoup container element
    
    Returns:
        float: Rating percentage value
    """
    rating_div = container.find('div', class_="rating-stars-yellow")
    style = rating_div['style']
    rating_str = style.split()[1]
    return float(rating_str[:-2])


def extract_laptop_data(container):
    """
    Extracts all relevant data from a laptop container.
    
    Args:
        container: BeautifulSoup container element
    
    Returns:
        dict: Dictionary containing name, price, rating, and votes
    """
    name = container.h4.a.text
    price = container.find('span', class_='amount').text
    rating = extract_rating(container)
    vote = container.find('div', class_="rating-num").text
    
    return {
        'name': name,
        'price': price,
        'rating': rating,
        'vote': vote
    }


def scrape_page(url, request_num, start_time):
    """
    Scrapes a single page and returns laptop containers.
    
    Args:
        url (str): URL to scrape
        request_num (int): Current request number
        start_time (float): Start time of scraping session
    
    Returns:
        list: List of laptop containers or None if error
    """
    response = get(url)
    
    # Monitor requests
    elapsed_time = time() - start_time
    print(f'Request: {request_num}; Frequency: {request_num/elapsed_time:.2f} requests/s')
    clear_output(wait=True)
    
    # Check status code
    if response.status_code != 200:
        warn(f'Request: {request_num}; Status code: {response.status_code}')
        return None
    
    # Parse HTML
    page_html = BeautifulSoup(response.text, 'html.parser')
    return page_html.find_all('div', class_='item-inner clearfix')


def scrape_all_laptops(config, build_url_func):
    """
    Scrapes all laptop data based on configuration.
    
    Args:
        config (dict): Configuration dictionary
        build_url_func (function): Function to build URLs
    
    Returns:
        dict: Dictionary containing lists of names, prices, ratings, and votes
    """
    names, prices, ratings, votes = [], [], [], []
    start_time = time()
    requests = 0
    
    for ram_size in config['ram_sizes']:
        for page in config['pages']:
            # Make request with random delay
            sleep(randint(config['sleep_min'], config['sleep_max']))
            requests += 1
            
            # Scrape page
            url = build_url_func(page, ram_size)
            containers = scrape_page(url, requests, start_time)
            
            if containers is None:
                continue
            
            # Extract data from containers
            for container in containers:
                # Only process laptops with ratings
                if container.find('div', class_='rating-stars-yellow') is not None:
                    data = extract_laptop_data(container)
                    names.append(data['name'])
                    prices.append(data['price'])
                    ratings.append(data['rating'])
                    votes.append(data['vote'])
            
            # Check if max requests exceeded
            if requests > config['max_requests']:
                warn('Number of requests was greater than expected.')
                return {'names': names, 'prices': prices, 'ratings': ratings, 'votes': votes}
    
    return {'names': names, 'prices': prices, 'ratings': ratings, 'votes': votes}
