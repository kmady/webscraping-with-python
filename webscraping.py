######################################################################################################################
# Author: Demdah
######################################################################################################################
''' 
This code is used to scrap data from the bestbuy website. On can adapt it to scrap data for his own purpose 
'''

from warnings import warn
from time import sleep

# Import custom modules
from config import get_config, build_url
from scraper import scrape_all_laptops
from data_cleaner import save_data, load_and_process_data
from visualizer import visualize_data


def main():
    """
    Main execution function that orchestrates the web scraping workflow.
    
    Workflow:
        1. Load configuration
        2. Scrape laptop data from BestBuy
        3. Save raw data to CSV
        4. Clean and process the data
        5. Visualize results with plots and statistics
    """
    warn("Warning Simulation")
    
    # Get configuration
    config = get_config()
    
    # Scrape data
    print("Starting web scraping...")
    data = scrape_all_laptops(config, build_url)
    
    # Wait before processing
    sleep(3)
    
    # Save raw data
    print("\nSaving data...")
    save_data(data, config['output_file'])
    
    # Load and clean data
    print("\nCleaning data...")
    df = load_and_process_data(config['output_file'])
    
    # Visualize results
    print("\nVisualizing data...")
    visualize_data(df)


if __name__ == '__main__':
    main()
