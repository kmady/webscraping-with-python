# Best Buy Canada Scraping Guide (2025)

## 🔍 Analysis Summary

I've analyzed the Best Buy Canada website and updated your scraping configuration. Here are my findings:

### Major Changes from Previous Version

1. **Website Architecture**: Best Buy Canada now uses a **React-based dynamic website**
2. **New HTML Structure**: Product containers and CSS classes have completely changed
3. **URL Structure**: The URL format is the same, but uses `custom0ramsize` for RAM filtering
4. **Data Format**: Ratings and reviews now use Schema.org microdata format

---

## 📊 Current Website Structure

### URL Format
```
https://www.bestbuy.ca/en-ca/category/windows-laptops/36711?page=1&path=category%3AComputers%2B%2526%2BTablets%3Bcategory%3ALaptops%2B%2526%2BMacBooks%3Bcategory%3AWindows%2BLaptops%3Bcustom0ramsize%3A8
```

### Key HTML Elements Found

| Data Field | HTML Selector | Notes |
|------------|--------------|-------|
| Product Container | `div[itemType="http://schema.org/Product"]` | Schema.org markup |
| Product Name | `h3.productItemName_3IZ3c` | Inside container |
| Price | `span.style-module_screenReaderOnly__4QmbS` | Most reliable |
| Rating | `meta[itemprop="ratingValue"]` | Inside aggregateRating |
| Review Count | `meta[itemprop="reviewCount"]` | Inside aggregateRating |

### Sample Product Data
- **Total Results**: 1,512 Windows laptops with 8GB RAM (as of Dec 2025)
- **Products per page**: ~24 items
- **Available RAM filters**: 8GB, 16GB, 32GB (most common)

---

## ⚙️ Updated Configuration

### Changes Made to `config.py`

1. **Reduced page count** (1-10 instead of 1-19) for safer testing
2. **Updated RAM sizes** to focus on common configurations (8, 16, 32 GB)
3. **Increased delays** between requests (10-20 seconds instead of 8-15)
4. **Added user agent** configuration for better request handling
5. **Changed output filename** to `laptops_bestbuy_2025.csv`

### Changes Made to `scraper.py`

1. **New product container selector**: Uses Schema.org `itemType` attribute
2. **Updated data extraction**:
   - Rating extraction from `<meta itemprop="ratingValue">`
   - Review count from `<meta itemprop="reviewCount">`
   - Price from screen-reader accessible elements
3. **Improved error handling** with fallback selectors
4. **Better logging** with detailed progress information

---

## ⚠️ Important Limitations & Recommendations

### 🚨 Critical Issue: JavaScript-Rendered Content

**Best Buy's website is React-based**, which means:
- Most content is loaded via JavaScript AFTER the initial HTML loads
- Simple HTTP requests (like `requests.get()`) may NOT get the full product data
- You might receive an empty or incomplete product list

### 📋 Recommended Solutions

#### Option 1: Use Selenium (Recommended for Reliability)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This will render JavaScript and get the full page
driver = webdriver.Chrome()
driver.get(url)
# Wait for products to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[itemtype*="Product"]'))
)
html = driver.page_source
# Then parse with BeautifulSoup
```

#### Option 2: Use Playwright (Modern Alternative)
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.wait_for_selector('div[itemtype*="Product"]')
    html = page.content()
    # Then parse with BeautifulSoup
```

#### Option 3: Test Current Setup First
The current implementation might still work if Best Buy serves some static HTML. Try it first:

```bash
cd /home/dem/workspace/webscraping-with-python
poetry run python src/webscraping.py
```

---

## 🎯 Testing Recommendations

### Step 1: Test with Minimal Configuration
Start with a very small test to see if the current approach works:

```python
# In config.py, temporarily set:
'pages': ['1'],  # Just one page
'ram_sizes': ['8'],  # Just one RAM size
'max_requests': 5  # Very low limit
```

### Step 2: Check the Output
After running, check:
1. **Log file**: Look for "Found X product containers" messages
2. **CSV file**: See if `data/laptops_bestbuy_2025.csv` has data
3. **Data quality**: Verify names, prices, ratings are extracted

### Step 3: Scale Up Gradually
If successful, gradually increase:
- Pages: 1 → 3 → 10
- RAM sizes: Add 16GB and 32GB
- Max requests: Increase to 50, then 100

---

## 📝 Usage Instructions

### Run the Scraper

```bash
# Navigate to project directory
cd /home/dem/workspace/webscraping-with-python

# Run the main scraper
poetry run python src/webscraping.py
```

### Expected Output Structure

The scraper will create a CSV file with:
- **name**: Full laptop product name
- **price**: Price as string (e.g., "$500.39")
- **rating**: Float value (0-5)
- **reviews**: Integer count of reviews

### Monitoring Progress

The scraper logs will show:
```
Request #1 | Frequency: 0.12 req/s | URL: https://www.bestbuy.ca...
Found 24 product containers on page
Extracted 24 laptops from this page
```

---

## 🛡️ Best Practices & Ethics

### Rate Limiting
- Current config: 10-20 seconds between requests
- **DO NOT** reduce this below 5 seconds
- Best Buy may block aggressive scrapers

### Respectful Scraping
1. ✅ Use appropriate User-Agent headers (already configured)
2. ✅ Respect robots.txt (check: https://www.bestbuy.ca/robots.txt)
3. ✅ Limit concurrent requests (current implementation is sequential)
4. ✅ Cache results to avoid re-scraping
5. ❌ Don't scrape during peak hours

### Legal Considerations
- Review Best Buy's Terms of Service
- This is for educational/analysis purposes
- Don't republish scraped data commercially
- Consider using Best Buy's official API if available

---

## 🐛 Troubleshooting

### Problem: No products found
**Cause**: JavaScript-rendered content
**Solution**: Use Selenium or Playwright (see Option 1/2 above)

### Problem: 403 Forbidden errors
**Cause**: Rate limiting or bot detection
**Solution**: 
- Increase delays between requests
- Rotate user agents
- Use proxy servers

### Problem: Incomplete data (missing ratings/reviews)
**Cause**: HTML structure changed or data not in initial load
**Solution**:
- Check the HTML source manually
- Update CSS selectors in `scraper.py`
- Use browser automation (Selenium)

### Problem: Incorrect prices
**Cause**: Currency formatting or sale prices
**Solution**: The price is extracted as-is; process in `data_cleaner.py`

---

## 📈 Next Steps

1. **Test the current setup** with minimal config
2. **Evaluate results** - if empty, you need JavaScript rendering
3. **Implement Selenium** if needed (I can help with this)
4. **Data cleaning**: Process prices, handle duplicates
5. **Analysis**: Use the visualization tools already in your project

---

## 🔧 Alternative: API Exploration

Best Buy might have an official API that's more reliable than scraping:
- Check: https://developer.bestbuy.com/ (US site, but Canada might have similar)
- Benefits: Structured data, no scraping needed, legal/supported
- Worth investigating before extensive scraping

---

## 📞 Support

If you encounter issues:
1. Check the log files in `src/logs/`
2. Verify the HTML structure hasn't changed (inspect page source)
3. Test with a single URL manually
4. Consider JavaScript rendering solutions

---

**Last Updated**: December 9, 2025
**Website Analyzed**: https://www.bestbuy.ca/en-ca/category/windows-laptops/36711
**Status**: Configuration updated, testing required
