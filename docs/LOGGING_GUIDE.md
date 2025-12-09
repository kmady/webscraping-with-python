# Logging Guide

## Overview

This project uses [Loguru](https://github.com/Delgan/loguru) for logging instead of traditional `print()` statements. Loguru provides better log formatting, automatic file rotation, and different log levels for better debugging and monitoring.

## Features

### Log Levels

The project uses the following log levels:

- **DEBUG**: Detailed information for debugging (e.g., request frequencies)
- **INFO**: General informational messages (e.g., "Starting web scraping...")
- **WARNING**: Warning messages (e.g., HTTP status code errors)
- **SUCCESS**: Success messages (e.g., "Data saved successfully")
- **ERROR**: Error messages (automatically captured)

### Log Outputs

Logs are written to two destinations:

1. **Console (stdout)**: Colorized logs with timestamps for real-time monitoring
2. **Log Files**: Persistent logs stored in `logs/webscraping_{date}.log`

### Log File Management

- **Rotation**: Log files are automatically rotated when they reach 500 MB
- **Retention**: Log files are kept for 10 days
- **Compression**: Old log files are compressed as `.zip` files
- **Location**: All logs are stored in the `logs/` directory (ignored by git)

## Logger Configuration

The logger is configured in `src/logger.py`:

```python
from logger import logger

# Use it throughout your code
logger.info("This is an info message")
logger.warning("This is a warning")
logger.error("This is an error")
logger.success("This is a success message")
logger.debug("This is debug info")
```

## Log Format

### Console Format
```
YYYY-MM-DD HH:mm:ss | LEVEL    | module:function:line - message
```

Example:
```
2024-12-08 22:00:00 | INFO     | webscraping:main:35 - Starting web scraping...
```

### File Format
```
YYYY-MM-DD HH:mm:ss | LEVEL    | module:function:line - message
```

## Migration from Print Statements

All `print()` statements have been replaced with appropriate logger calls:

| Old Code | New Code | Reason |
|----------|----------|--------|
| `print("Starting...")` | `logger.info("Starting...")` | General information |
| `print(f"Request: {n}")` | `logger.debug(f"Request: {n}")` | Debugging info |
| `warn("Error!")` | `logger.warning("Error!")` | Warning message |
| `print(df.info())` | `logger.debug(f"{df.info()}")` | Debug information |

## Benefits

1. **Structured Logging**: Consistent format with timestamps and log levels
2. **File Persistence**: Logs are saved to files for later analysis
3. **Automatic Rotation**: No manual log file management needed
4. **Color Coding**: Console output is color-coded by severity
5. **Performance**: More efficient than print statements
6. **Debugging**: Easy to filter logs by level (INFO, DEBUG, etc.)

## Usage Examples

### In webscraping.py
```python
from logger import logger

logger.info("Starting web scraping...")
logger.info("Saving data...")
logger.info("Cleaning data...")
```

### In scraper.py
```python
from logger import logger

logger.debug(f'Request: {request_num}; Frequency: {freq:.2f} requests/s')
logger.warning(f'Request: {request_num}; Status code: {status}')
```

### In data_cleaner.py
```python
from logger import logger

logger.info(f"DataFrame created with {len(df)} rows")
logger.success(f"Data saved to {filename}")
```

## Viewing Logs

### Real-time (Console)
Run the scraper normally and watch colorized logs in the terminal.

### Historical (Log Files)
```bash
# View latest log file
cat logs/webscraping_2024-12-08.log

# Search for warnings
grep WARNING logs/webscraping_2024-12-08.log

# Search for errors
grep ERROR logs/*.log
```

## Configuration

To modify logging behavior, edit `src/logger.py`:

- Change log level: Modify `level="INFO"` to `"DEBUG"` for more verbose output
- Change rotation size: Modify `rotation="500 MB"`
- Change retention period: Modify `retention="10 days"`
- Disable file logging: Remove or comment out the second `logger.add()` call
