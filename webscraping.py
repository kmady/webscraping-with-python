######################################################################################################################
# Author: Demdah
######################################################################################################################
''' 
This code is used to scrap data from the bestbuy website. On can adapt it to scrap data for his own purpose 
'''

from requests import get
from bs4 import BeautifulSoup
from IPython.core.display import clear_output
from warnings import warn
warn("Warning Simulation")
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
from random import randint
from time import time

# After identifying the parameters we will used to do my research I define the following function  to get the url needed
# The first parameter is the page number and the second one ins RAM size.

def URL(s,t):
    url = 'https://www.bestbuy.ca/en-ca/category/laptops-macbooks/20352.aspx?type=product&page='+s+'&filter=category%253aComputers%2B%2526%2BTablets%253bcategory%253aLaptops%2B%2526%2BMacBooks%253bcustom0ramsize%253a8'+ t    
   return url 
# I select the following list of pages and the RAM size list.
pages = [str(i) for i in range(1,20)]
Ram_url = ['2', '4',  '8', '12', '16','32', '64']

# Redeclaring the lists to store data in
names = []
prices = []
ratings = []
votes = []

# Preparing the monitoring of the loop
start_time = time()
requests = 0

# For every number of Go of ram in Ram_url
for t in Ram_url:

    # For every page in the interval 1-20
    for s in pages:

        # Make a get request
        response = get(URL(s, t))
       

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 200:
            warn('Number of requests was greater than expected.')  
            break 

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the laptop containers from a single page
        laptops_containers = page_html.find_all('div',  class_='item-inner clearfix')

        # For every computer in laptops_container
        for container in laptops_containers:
            # If the computer has a rating, then:
            if container.find('div',  class_='rating-stars-yellow') is not None:

                # Scrape the name
                name = container.h4.a.text
                names.append(name)

                # Scrape the price 
                price = container.find('span', class_='amount').text
                prices.append(price)

                # Scrape the rating
                rating = Rating(container)
                ratings.append(rating)

                
                # Scrape the number of votes
                vote = container.find('div', class_="rating-num").text
                votes.append(vote)

# I construct the dataframe of my data with pandas
laptops_rating = pd.DataFrame({'laptops': names,
                       'prices': prices,
                       'ratings': ratings,
                        'votes': votes})
                    
# Data info
print(laptops_rating.info())

# Save the dataframe in csv.
laptops_rating.to_csv('laptops_rating2019.csv')

# I define the following function to clean the price column.
def price(x):
    if ',' in x:
        x = x.replace(',','')
        return float(x[1:])
    else:
        return float(x[1:])
# Clean the prices column
df['prices'] = [prix(x) for x in df['prices']]

# The following function is to clean votes column
def Remove_parenthese(x):
    y = len(x)-1
    z = x[1:y]
    z = float(z)
    return z

# Clean the votes column
df['votes'] = [Remove_parenthese(x) for x in df['votes']]

print('#'*100)
print('Descriptive statistic measures of the data')
print(df[['prices', 'ratings', 'votes']].describe())

# Plot tghe histogram
df[['prices', 'ratings', 'votes']].hist(bins=15, figsize = (16,8))
plt.show()

# Plot the boxplots
fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (16,4))
ax1, ax2, ax3 = fig.axes

ax1.boxplot(df['prices']) # bin range = 1
ax1.set_title('Prices')

ax2.boxplot(df['ratings']) # bin range = 10
ax2.set_title('Ratings')

ax3.boxplot(df['votes'])
ax3.set_title('Votes')

for ax in fig.axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.show()