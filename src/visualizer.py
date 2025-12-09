"""
Data visualization module for laptop data analysis.

Enhanced with beautiful, modern styling and comprehensive visualizations.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from loguru import logger

# Set the style for all plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def create_histograms(df):
    """
    Creates beautiful histograms for prices, ratings, and votes with enhanced styling.
    
    Args:
        df (pd.DataFrame): Dataframe containing the data
    """
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))
    fig.suptitle('Distribution Analysis', fontsize=20, fontweight='bold', y=1.02)
    
    # Define colors
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    # Prices histogram
    axes[0].hist(df['prices'], bins=20, color=colors[0], alpha=0.7, edgecolor='black', linewidth=1.2)
    axes[0].set_title('Laptop Prices Distribution', fontsize=14, fontweight='bold', pad=10)
    axes[0].set_xlabel('Price ($)', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Frequency', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3, linestyle='--')
    axes[0].axvline(df['prices'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${df["prices"].mean():.2f}')
    axes[0].axvline(df['prices'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: ${df["prices"].median():.2f}')
    axes[0].legend(fontsize=10)
    
    # Ratings histogram
    axes[1].hist(df['ratings'], bins=20, color=colors[1], alpha=0.7, edgecolor='black', linewidth=1.2)
    axes[1].set_title('Customer Ratings Distribution', fontsize=14, fontweight='bold', pad=10)
    axes[1].set_xlabel('Rating (0-5)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Frequency', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3, linestyle='--')
    axes[1].axvline(df['ratings'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["ratings"].mean():.2f}')
    axes[1].axvline(df['ratings'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["ratings"].median():.2f}')
    axes[1].legend(fontsize=10)
    
    # Votes histogram
    axes[2].hist(df['votes'], bins=20, color=colors[2], alpha=0.7, edgecolor='black', linewidth=1.2)
    axes[2].set_title('Review Counts Distribution', fontsize=14, fontweight='bold', pad=10)
    axes[2].set_xlabel('Number of Reviews', fontsize=12, fontweight='bold')
    axes[2].set_ylabel('Frequency', fontsize=12, fontweight='bold')
    axes[2].grid(True, alpha=0.3, linestyle='--')
    axes[2].axvline(df['votes'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["votes"].mean():.2f}')
    axes[2].axvline(df['votes'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["votes"].median():.2f}')
    axes[2].legend(fontsize=10)
    
    plt.tight_layout()
    plt.show()


def create_boxplots(df):
    """
    Creates beautiful boxplots for prices, ratings, and votes with enhanced styling.
    
    Args:
        df (pd.DataFrame): Dataframe containing the data
    """
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
    fig.suptitle('Statistical Distribution Analysis (Boxplots)', fontsize=20, fontweight='bold', y=1.02)
    
    # Define colors
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    # Prices boxplot
    bp1 = axes[0].boxplot(df['prices'], patch_artist=True, widths=0.6,
                          boxprops=dict(facecolor=colors[0], alpha=0.7, linewidth=2),
                          medianprops=dict(color='darkred', linewidth=2),
                          whiskerprops=dict(linewidth=2),
                          capprops=dict(linewidth=2),
                          flierprops=dict(marker='o', markerfacecolor='red', markersize=8, alpha=0.5))
    axes[0].set_title('Laptop Prices', fontsize=14, fontweight='bold', pad=10)
    axes[0].set_ylabel('Price ($)', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y', linestyle='--')
    axes[0].set_xticklabels(['Prices'])
    
    # Ratings boxplot
    bp2 = axes[1].boxplot(df['ratings'], patch_artist=True, widths=0.6,
                          boxprops=dict(facecolor=colors[1], alpha=0.7, linewidth=2),
                          medianprops=dict(color='darkred', linewidth=2),
                          whiskerprops=dict(linewidth=2),
                          capprops=dict(linewidth=2),
                          flierprops=dict(marker='o', markerfacecolor='red', markersize=8, alpha=0.5))
    axes[1].set_title('Customer Ratings', fontsize=14, fontweight='bold', pad=10)
    axes[1].set_ylabel('Rating (0-5)', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y', linestyle='--')
    axes[1].set_xticklabels(['Ratings'])
    
    # Votes boxplot
    bp3 = axes[2].boxplot(df['votes'], patch_artist=True, widths=0.6,
                          boxprops=dict(facecolor=colors[2], alpha=0.7, linewidth=2),
                          medianprops=dict(color='darkred', linewidth=2),
                          whiskerprops=dict(linewidth=2),
                          capprops=dict(linewidth=2),
                          flierprops=dict(marker='o', markerfacecolor='red', markersize=8, alpha=0.5))
    axes[2].set_title('Review Counts', fontsize=14, fontweight='bold', pad=10)
    axes[2].set_ylabel('Number of Reviews', fontsize=12, fontweight='bold')
    axes[2].grid(True, alpha=0.3, axis='y', linestyle='--')
    axes[2].set_xticklabels(['Votes'])
    
    # Remove top and right spines for cleaner look
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)
    
    plt.tight_layout()
    plt.show()


def create_scatter_plots(df):
    """
    Creates scatter plots to show relationships between variables.
    
    Args:
        df (pd.DataFrame): Dataframe containing the data
    """
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))
    fig.suptitle('Relationship Analysis', fontsize=20, fontweight='bold', y=1.02)
    
    # Price vs Rating scatter
    axes[0].scatter(df['prices'], df['ratings'], c=df['votes'], cmap='viridis', 
                    alpha=0.6, s=100, edgecolors='black', linewidth=1)
    axes[0].set_title('Price vs Rating', fontsize=14, fontweight='bold', pad=10)
    axes[0].set_xlabel('Price ($)', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Rating (0-5)', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3, linestyle='--')
    cbar1 = plt.colorbar(axes[0].collections[0], ax=axes[0])
    cbar1.set_label('Number of Reviews', fontsize=11, fontweight='bold')
    
    # Price vs Votes scatter
    axes[1].scatter(df['prices'], df['votes'], c=df['ratings'], cmap='coolwarm', 
                    alpha=0.6, s=100, edgecolors='black', linewidth=1)
    axes[1].set_title('Price vs Review Count', fontsize=14, fontweight='bold', pad=10)
    axes[1].set_xlabel('Price ($)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Number of Reviews', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3, linestyle='--')
    cbar2 = plt.colorbar(axes[1].collections[0], ax=axes[1])
    cbar2.set_label('Rating', fontsize=11, fontweight='bold')
    
    # Remove top and right spines
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)
    
    plt.tight_layout()
    plt.show()


def create_correlation_heatmap(df):
    """
    Creates a correlation heatmap for the numerical variables.
    
    Args:
        df (pd.DataFrame): Dataframe containing the data
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Calculate correlation matrix
    corr = df[['prices', 'ratings', 'votes']].corr()
    
    # Create heatmap
    sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                square=True, linewidths=2, cbar_kws={"shrink": 0.8},
                annot_kws={'size': 14, 'weight': 'bold'}, ax=ax)
    
    ax.set_title('Correlation Matrix Heatmap', fontsize=18, fontweight='bold', pad=20)
    
    # Customize tick labels
    ax.set_xticklabels(['Prices', 'Ratings', 'Reviews'], fontsize=12, fontweight='bold')
    ax.set_yticklabels(['Prices', 'Ratings', 'Reviews'], fontsize=12, fontweight='bold', rotation=0)
    
    plt.tight_layout()
    plt.show()


def create_summary_stats_plot(df):
    """
    Creates a visual summary of key statistics.
    
    Args:
        df (pd.DataFrame): Dataframe containing the data
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    # Create summary statistics
    stats_text = f"""
    📊 LAPTOP DATA SUMMARY STATISTICS
    {'='*60}
    
    💰 PRICES:
       • Mean:        ${df['prices'].mean():.2f}
       • Median:      ${df['prices'].median():.2f}
       • Std Dev:     ${df['prices'].std():.2f}
       • Min:         ${df['prices'].min():.2f}
       • Max:         ${df['prices'].max():.2f}
       • Range:       ${df['prices'].max() - df['prices'].min():.2f}
    
    ⭐ RATINGS:
       • Mean:        {df['ratings'].mean():.2f} / 5.0
       • Median:      {df['ratings'].median():.2f} / 5.0
       • Std Dev:     {df['ratings'].std():.2f}
       • Min:         {df['ratings'].min():.2f}
       • Max:         {df['ratings'].max():.2f}
    
    📝 REVIEWS:
       • Mean:        {df['votes'].mean():.0f} reviews
       • Median:      {df['votes'].median():.0f} reviews
       • Std Dev:     {df['votes'].std():.0f}
       • Min:         {df['votes'].min():.0f}
       • Max:         {df['votes'].max():.0f}
    
    📦 DATASET:
       • Total Laptops: {len(df)}
    """
    
    ax.text(0.1, 0.5, stats_text, fontsize=13, family='monospace',
            verticalalignment='center', bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.5, pad=1))
    
    plt.title('Statistical Summary', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.show()


def visualize_data(df):
    """
    Creates all enhanced visualizations for the data.
    
    Args:
        df (pd.DataFrame): Dataframe containing the data
    """
    logger.info('=' * 100)
    logger.info('📊 CREATING BEAUTIFUL VISUALIZATIONS...')
    logger.info('=' * 100)
    logger.info('Descriptive statistic measures of the data')
    logger.info(f"\n{df[['prices', 'ratings', 'votes']].describe()}")
    logger.info('=' * 100)
    
    # Create all visualizations
    create_histograms(df)
    create_boxplots(df)
    create_scatter_plots(df)
    create_correlation_heatmap(df)
    create_summary_stats_plot(df)
    
    logger.success('✨ All visualizations created successfully!')
