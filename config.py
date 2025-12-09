"""
Configuration module for web scraping parameters.
"""


def get_config():
    """
    Returns configuration parameters for web scraping.
    
    Returns:
        dict: Configuration dictionary with scraping parameters
    """
    return {
        'pages': [str(i) for i in range(1, 20)],
        'ram_sizes': ['2', '4', '8', '12', '16', '32', '64'],
        'sleep_min': 8,
        'sleep_max': 15,
        'max_requests': 200,
        'output_file': 'laptops_rating2019.csv'
    }


def build_url(page_number, ram_size):
    """
    Builds the URL for BestBuy laptop search with specific page and RAM size.
    
    Args:
        page_number (str): Page number to scrape
        ram_size (str): RAM size filter (in GB)
    
    Returns:
        str: Complete URL for the search
    """
    base_url = 'https://www.bestbuy.ca/en-ca/category/laptops-macbooks/20352.aspx'
    params = f'?type=product&page={page_number}'
    filters = f'&filter=category%253aComputers%2B%2526%2BTablets%253bcategory%253aLaptops%2B%2526%2BMacBooks%253bcustom0ramsize%253a8{ram_size}'
    return base_url + params + filters
