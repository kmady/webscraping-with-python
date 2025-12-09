"""
Script to visualize existing laptop data from CSV file.

This script loads the laptops_bestbuy_2025.csv file and creates beautiful visualizations.
"""

import sys
sys.path.append('src')

from data_cleaner import load_and_process_data
from visualizer import visualize_data
from loguru import logger


def main():
    """
    Main function to load and visualize existing data.
    """
    # Path to the CSV file
    csv_file = 'data/laptops_bestbuy_2025.csv'
    
    logger.info(f"Loading data from {csv_file}...")
    
    try:
        # Load and clean the data
        df = load_and_process_data(csv_file)
        
        logger.info(f"Successfully loaded {len(df)} laptops")
        logger.info(f"\nDataframe shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")
        
        # Create visualizations
        logger.info("\nCreating visualizations...")
        visualize_data(df)
        
        logger.success("Visualization complete!")
        
    except FileNotFoundError:
        logger.error(f"File not found: {csv_file}")
        logger.error("Please make sure the file exists or run the scraper first.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
