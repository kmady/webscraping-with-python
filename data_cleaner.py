"""
Data cleaning module for processing scraped laptop data.
"""

import pandas as pd


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
    
    Args:
        vote_str (str): Vote string (e.g., '(123)')
    
    Returns:
        float: Cleaned vote count
    """
    return float(vote_str[1:-1])


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
        'votes': data['votes']
    })
    
    print(df.info())
    df.to_csv(filename)
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
