# Zillow Agent Scraper

A Python-based web scraper for extracting real estate agent information from Zillow using Selenium.

## Overview

This project consists of two main scripts:
- **agent.py** - Scrapes agent listing pages by ZIP code to collect agent profile URLs
- **agent_item.py** - Scrapes individual agent profiles for detailed information

## Features

- Scrapes agent profiles from Zillow by ZIP code
- Extracts detailed agent information including:
  - Headshot URL
  - Sales statistics (last 12 months, total sales)
  - Rental information (price range, average price)
  - License number
- Uses proxy support for reliable scraping
- Saves data to CSV format

## Requirements

- Python 3.x
- Chrome browser
- Required packages (see requirements.txt):
  - selenium-wire
  - webdriver-manager
  - beautifulsoup4

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Scrape Agent URLs

Run `agent.py` to collect agent profile URLs by ZIP code:

```bash
python agent.py
```

You will be prompted to enter:
- Postal code (ZIP code)
- First page number to start scraping from

This will create a CSV file named `agents_{zipcode}.csv` containing agent URLs.

### Step 2: Scrape Agent Details

Run `agent_item.py` to scrape detailed information from agent profiles:

```bash
python agent_item.py
```

You will be prompted to enter:
- CSV filename (without .csv extension) containing the agent URLs

This will create `agents_data.csv` with detailed agent information.

## Output Files

- `agents_{zipcode}.csv` - Contains agent profile URLs
- `agents_data.csv` - Contains detailed agent information

## Configuration

The scripts use Oxylabs proxy configuration. Update the proxy credentials in both scripts if needed:
```python
proxy_host = 'us-pr.oxylabs.io'
proxy_port = 10000
username = 'your_username'
password = 'your_password'
```

## Notes

- The scraper includes delays to avoid overwhelming the server
- Chrome WebDriver is automatically managed via webdriver-manager
- Data is appended to CSV files to allow resuming interrupted scrapes

## Disclaimer

This tool is for educational purposes only. Make sure to review and comply with Zillow's Terms of Service and robots.txt before scraping.

