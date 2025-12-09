# Selenium Setup and Usage Guide

## 🚀 Quick Start

Follow these steps to install and run the Selenium-based Best Buy scraper:

### Step 1: Install Dependencies

```bash
cd /home/dem/workspace/webscraping-with-python

# Install all dependencies including Selenium
poetry install
```

This will install:
- `selenium` - Web automation framework
- `webdriver-manager` - Automatic ChromeDriver management (no manual download needed!)
- All other existing dependencies

### Step 2: Install Chrome/Chromium Browser

The scraper uses Chrome, so you need to have it installed:

**For Debian/Ubuntu Linux:**
```bash
# Install Chromium browser
sudo apt update
sudo apt install -y chromium-browser chromium-chromedriver

# OR install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

**Check if Chrome is installed:**
```bash
google-chrome --version
# OR
chromium-browser --version
```

### Step 3: Run the Scraper!

```bash
# Run the main scraping script
poetry run python src/webscraping.py
```

That's it! The scraper will:
1. Automatically download the correct ChromeDriver version
2. Launch Chrome in headless mode (no GUI)
3. Scrape Best Buy Canada for laptop data
4. Save results to `data/laptops_bestbuy_2025.csv`

---

## 🎛️ Configuration Options

### Adjust Scraping Parameters

Edit `src/config.py` to customize:

```python
# Scrape fewer pages for testing
'pages': ['1'],  # Just page 1

# Focus on specific RAM sizes
'ram_sizes': ['8'],  # Just 8GB RAM

# Limit total requests
'max_requests': 10,  # Stop after 10 requests

# Adjust delays (seconds)
'sleep_min': 5,
'sleep_max': 10,
```

### Run with Browser Visible (Debug Mode)

To see what the scraper is doing, modify `src/scraper_selenium.py`:

```python
# Change this line in scrape_all_laptops function:
scraper = BestBuySeleniumScraper(config, headless=False)  # Set to False
```

This will show the Chrome browser window during scraping.

---

## 📊 Expected Output

### Console Output

```
Setting up Chrome WebDriver...
Running in headless mode (no browser window)
Chrome WebDriver initialized successfully
============================================================
Starting Best Buy Canada laptop scraping with Selenium...
Pages to scrape: ['1', '2', '3', ...]
RAM sizes to filter: ['8', '16', '32']
============================================================

--- Scraping RAM size: 8GB ---
Request #1 | Loading: https://www.bestbuy.ca/en-ca/category/windows-laptops/36711?page=1...
Request #1 | Found 24 products | Frequency: 0.12 req/s
✓ Extracted 24 laptops from this page

Sleeping for 12 seconds...
Request #2 | Loading: https://www.bestbuy.ca/en-ca/category/windows-laptops/36711?page=2...
Request #2 | Found 24 products | Frequency: 0.08 req/s
✓ Extracted 24 laptops from this page

...

============================================================
SCRAPING COMPLETED!
Total requests: 30
Total laptops extracted: 720
Total time: 385.23 seconds
Average time per request: 12.84 seconds
============================================================
```

### Output File

**Location**: `data/laptops_bestbuy_2025.csv`

**Format**:
```csv
name,price,rating,reviews
"HP 15.6"" Laptop - Silver (Intel Core i5-1235U/512GB SSD/8GB RAM/Windows 11)",$699.99,4.5,234
"Lenovo IdeaPad 3 15.6"" Laptop - Grey (AMD Ryzen 5/256GB SSD/8GB RAM)",$549.99,4.2,156
...
```

---

## 🔧 Troubleshooting

### Problem: ChromeDriver Error

**Error**: `selenium.common.exceptions.SessionNotCreatedException`

**Solution**:
```bash
# Update webdriver-manager
poetry add webdriver-manager@latest

# Or manually install ChromeDriver
sudo apt install chromium-chromedriver
```

### Problem: Chrome Not Found

**Error**: `selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH`

**Solution**:
```bash
# Install Chrome/Chromium
sudo apt update
sudo apt install chromium-browser
```

### Problem: No Products Found

**Error**: Logs show "No products found or timeout"

**Possible Causes**:
1. Website structure changed - inspect the page and update CSS selectors
2. Anti-bot measures - try increasing delays or using different user agents
3. Network issues - check internet connection

**Debug**:
```python
# Run with visible browser to see what's happening
scraper = BestBuySeleniumScraper(config, headless=False)
```

### Problem: Permission Denied on Linux

**Error**: `selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start`

**Solution**:
```bash
# Add --no-sandbox flag (already included in code)
# Or run with proper permissions
chmod +x /path/to/chromedriver
```

### Problem: Slow Performance

**Solutions**:
1. Increase `sleep_min` and `sleep_max` to avoid rate limiting
2. Reduce number of pages in config
3. Scrape during off-peak hours

---

## 🎯 Testing Recommendations

### Minimal Test Configuration

For initial testing, use this in `src/config.py`:

```python
SCRAPING_CONFIG = {
    'base_url': 'https://www.bestbuy.ca/en-ca/category/windows-laptops/36711',
    'pages': ['1'],  # JUST ONE PAGE
    'ram_sizes': ['8'],  # JUST ONE RAM SIZE
    'max_requests': 5,  # LOW LIMIT
    'sleep_min': 5,
    'sleep_max': 10,
    'timeout': 30,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'output_file': 'data/laptops_bestbuy_2025_test.csv'  # Test file
}
```

Run the test:
```bash
poetry run python src/webscraping.py
```

Check the results:
```bash
# View the CSV file
cat data/laptops_bestbuy_2025_test.csv

# Count extracted products
wc -l data/laptops_bestbuy_2025_test.csv
```

---

## 📈 Scaling Up

Once testing is successful, gradually increase:

### Phase 1: Multiple Pages, One RAM Size
```python
'pages': ['1', '2', '3'],
'ram_sizes': ['8'],
'max_requests': 10,
```

### Phase 2: Multiple RAM Sizes
```python
'pages': ['1', '2', '3'],
'ram_sizes': ['8', '16'],
'max_requests': 20,
```

### Phase 3: Full Scrape
```python
'pages': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
'ram_sizes': ['8', '16', '32'],
'max_requests': 100,  # Or higher
```

**Estimated Time**:
- 10 pages × 3 RAM sizes = 30 requests
- ~15 seconds per request (including delays)
- **Total: ~7-8 minutes**

---

## 🔒 Best Practices

### Respectful Scraping

1. **Use appropriate delays** (10-20 seconds between requests)
2. **Don't overwhelm the server** - scrape during off-peak hours
3. **Cache your results** - don't re-scrape unless necessary
4. **Monitor for rate limiting** - if you get blocked, increase delays

### Legal Considerations

- ✅ This is for **educational/personal analysis** purposes
- ❌ Don't use scraped data commercially without permission
- ✅ Check Best Buy's `robots.txt` and Terms of Service
- ✅ Consider using Best Buy's official API if available

### Performance Tips

1. **Headless mode** is faster than visible browser
2. **Disable images** in Chrome options (optional):
   ```python
   prefs = {"profile.managed_default_content_settings.images": 2}
   chrome_options.add_experimental_option("prefs", prefs)
   ```
3. **Parallel scraping** (advanced) - use multiple browsers, but be careful!

---

## 🆚 Selenium vs Requests Comparison

| Feature | Requests Library | Selenium |
|---------|-----------------|----------|
| **Speed** | ⚡ Fast (2-3 sec/page) | 🐢 Slower (10-15 sec/page) |
| **JavaScript** | ❌ No support | ✅ Full support |
| **Detection** | 🔴 Easily detected | 🟢 Harder to detect |
| **Resource Usage** | 💚 Low | 🔴 High (Chrome browser) |
| **Best Buy 2025** | ❌ Won't work (React) | ✅ Works perfectly |

**Verdict**: For Best Buy Canada's React-based website, **Selenium is required**.

---

## 🔄 Switching Back to Requests (If Needed)

If you want to switch back to the old requests-based scraper:

```python
# In src/webscraping.py, change:
from scraper_selenium import scrape_all_laptops

# To:
from scraper import scrape_all_laptops
```

---

## 📚 Additional Resources

- **Selenium Documentation**: https://selenium-python.readthedocs.io/
- **WebDriver Manager**: https://github.com/SergeyPirogov/webdriver_manager
- **Chrome DevTools**: Press F12 in browser to inspect HTML structure
- **Python Poetry**: https://python-poetry.org/docs/

---

## 🐛 Getting Help

If you encounter issues:

1. **Check the logs** in `src/logs/` directory
2. **Run with visible browser** (headless=False) to debug
3. **Verify Chrome installation**: `google-chrome --version`
4. **Check internet connection** and Best Buy website accessibility
5. **Review console output** for specific error messages

---

## ✅ Success Checklist

Before running the full scraper:

- [ ] Poetry dependencies installed (`poetry install`)
- [ ] Chrome/Chromium browser installed
- [ ] Tested with minimal configuration (1 page, 1 RAM size)
- [ ] Verified CSV output contains data
- [ ] Adjusted delays to be respectful (10-20 seconds)
- [ ] Set appropriate max_requests limit
- [ ] Checked available disk space for data storage

---

**Last Updated**: December 9, 2025  
**Selenium Version**: 4.16.0  
**Compatible with**: Best Buy Canada (2025)  
**Status**: Ready to use! 🎉
