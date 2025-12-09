"""
Configuration module for web scraping parameters.

Updated for the NEW Best Buy Canada website structure (2025).
URL: https://www.bestbuy.ca/en-ca/category/windows-laptops/36711
"""


def get_config():
    """
    Returns configuration parameters for web scraping.
    
    IMPORTANT NOTES:
    - Best Buy Canada has a React-based dynamic website
    - The page filter now uses 'custom0ramsize' for RAM filtering
    - Page numbers are simple: ?page=1, ?page=2, etc.
    - The website may require JavaScript rendering for full content
    
    Configuration includes:
    - pages: List of page numbers to scrape (1-10 recommended for testing)
    - ram_sizes: RAM size filters in GB (8, 16, 32 are most common)
    - sleep_min/max: Random delay between requests (10-20 seconds to be respectful)
    - max_requests: Maximum number of requests to prevent overloading
    - output_file: CSV filename for scraped data
    - user_agent: Modern browser user agent string
    
    Returns:
        dict: Configuration dictionary with scraping parameters
    """
    return {
        'pages': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],  # Pages 1-20
        'ram_sizes': ['8', '12', '32'],  # RAM sizes: 8GB, 12GB, and 32GB
        'sleep_min': 5,  # Minimum seconds between requests (be respectful)
        'sleep_max': 8,  # Maximum seconds between requests
        'max_requests': 65,  # Safety limit (3 RAM sizes × 20 pages = 60 requests + buffer)
        'output_file': 'data/laptops_bestbuy_2025.csv',  # New filename for new data
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'timeout': 30  # Request timeout in seconds
    }


def build_url(page_number, ram_size):
    """
    Builds the URL for BestBuy Windows laptop search with specific page and RAM size.
    
    Updated for the NEW Best Buy Canada URL structure (2025).
    
    Args:
        page_number (str): Page number to scrape
        ram_size (str): RAM size filter (in GB)
    
    Returns:
        str: Complete URL for the search
    
    Example:
        >>> build_url('1', '8')
        'https://www.bestbuy.ca/en-ca/category/windows-laptops/36711?page=1&path=category%3AComputers%2B%2526%2BTablets%3Bcategory%3ALaptops%2B%2526%2BMacBooks%3Bcategory%3AWindows%2BLaptops%3Bcustom0ramsize%3A8'
    
    Notes:
        - The URL uses URL-encoded path parameters
        - custom0ramsize is the RAM filter parameter
        - The path includes the full category hierarchy
    """
    base_url = 'https://www.bestbuy.ca/en-ca/category/windows-laptops/36711'
    params = f'?page={page_number}'
    # URL-encoded path: category:Computers+&+Tablets;category:Laptops+&+MacBooks;category:Windows+Laptops;custom0ramsize:{ram_size}
    filters = f'&path=category%3AComputers%2B%2526%2BTablets%3Bcategory%3ALaptops%2B%2526%2BMacBooks%3Bcategory%3AWindows%2BLaptops%3Bcustom0ramsize%3A{ram_size}'
    return base_url + params + filters


def get_alternative_url_no_ram_filter(page_number):
    """
    Alternative URL builder without RAM filtering.
    Use this if RAM filtering causes issues or for broader data collection.
    
    Args:
        page_number (str): Page number to scrape
    
    Returns:
        str: URL without RAM filter
    
    Example:
        >>> get_alternative_url_no_ram_filter('1')
        'https://www.bestbuy.ca/en-ca/category/windows-laptops/36711?page=1'
    """
    base_url = 'https://www.bestbuy.ca/en-ca/category/windows-laptops/36711'
    return f'{base_url}?page={page_number}'
