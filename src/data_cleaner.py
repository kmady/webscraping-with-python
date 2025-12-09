"""
Data cleaning module for processing scraped laptop data.
"""

import pandas as pd
from loguru import logger


def clean_price(price_str):
    """
    Cleans price string and converts to float.
    
    Args:
        price_str (str): Price string (e.g., '$1,234.56')
    
    Returns:
        float: Cleaned price value
    """
    if ',' in price_str:
        price_str = price_str.replace(',', '')
    return float(price_str[1:])


def clean_votes(vote_str):
    """
    Removes parentheses from votes string and converts to float.
    Handles both old format '(123)' and new format where it's already a number.
    
    Args:
        vote_str (str or int or float): Vote string (e.g., '(123)') or number
    
    Returns:
        float: Cleaned vote count
    """
    # If already a number, return it
    if isinstance(vote_str, (int, float)):
        return float(vote_str) if not pd.isna(vote_str) else 0.0
    # If string with parentheses, remove them
    if isinstance(vote_str, str) and vote_str.startswith('('):
        return float(vote_str[1:-1])
    # Otherwise try to convert directly
    try:
        return float(vote_str)
    except:
        return 0.0


def clean_dataframe(df):
    """
    Cleans the dataframe by processing prices and votes columns.
    
    Args:
        df (pd.DataFrame): Raw dataframe
    
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    df['prices'] = df['prices'].apply(clean_price)
    df['votes'] = df['votes'].apply(clean_votes)
    return df


def save_data(data, filename):
    """
    Saves scraped data to CSV file.
    
    Args:
        data (dict): Dictionary containing laptop data
        filename (str): Output filename
    
    Returns:
        pd.DataFrame: Created dataframe
    """
    df = pd.DataFrame({
        'laptops': data['names'],
        'prices': data['prices'],
        'ratings': data['ratings'],
        'votes': data.get('reviews', data.get('votes', None))  # Support both new ('reviews') and old ('votes') format
    })
    
    logger.info(f"DataFrame created with {len(df)} rows and {len(df.columns)} columns")
    logger.debug(f"DataFrame info:\n{df.info()}")
    df.to_csv(filename)
    logger.success(f"Data saved to {filename}")
    return df


def load_and_process_data(filename):
    """
    Loads data from CSV and processes it.
    
    Args:
        filename (str): Input CSV filename
    
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    df = pd.read_csv(filename)
    return clean_dataframe(df)
