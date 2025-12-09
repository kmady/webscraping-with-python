"""
Data visualization module for laptop data analysis.
"""

import matplotlib.pyplot as plt
from loguru import logger


def create_histograms(df):
    """
    Creates histograms for prices, ratings, and votes.
    
    Args:
        df (pd.DataFrame): Dataframe containing the data
    """
    df[['prices', 'ratings', 'votes']].hist(bins=15, figsize=(16, 8))
    plt.show()


def create_boxplots(df):
    """
    Creates boxplots for prices, ratings, and votes.
    
    Args:
        df (pd.DataFrame): Dataframe containing the data
    """
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(16, 4))
    ax1, ax2, ax3 = fig.axes
    
    ax1.boxplot(df['prices'])
    ax1.set_title('Prices')
    
    ax2.boxplot(df['ratings'])
    ax2.set_title('Ratings')
    
    ax3.boxplot(df['votes'])
    ax3.set_title('Votes')
    
    for ax in fig.axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    plt.show()


def visualize_data(df):
    """
    Creates all visualizations for the data.
    
    Args:
        df (pd.DataFrame): Dataframe containing the data
    """
    logger.info('=' * 100)
    logger.info('Descriptive statistic measures of the data')
    logger.info(f"\n{df[['prices', 'ratings', 'votes']].describe()}")
    
    create_histograms(df)
    create_boxplots(df)
