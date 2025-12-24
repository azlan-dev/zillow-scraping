# Zillow Agent Scraper

A Python web scraper for extracting real estate agent information from Zillow.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

**Step 1: Get Agent URLs**

```bash
python agent.py
```
- Enter ZIP code
- Enter starting page number
- Output: `agents_{zipcode}.csv`

**Step 2: Get Agent Details**

```bash
python agent_item.py
```
- Enter CSV filename (without .csv)
- Output: `agents_data.csv`

## Data Collected

- Headshot URL
- Sales statistics
- Rental information
- License number

## Configuration

Update proxy credentials in both scripts if needed:
```python
proxy_host = 'us-pr.oxylabs.io'
proxy_port = 10000
username = 'your_username'
password = 'your_password'
```

## Note

For educational purposes only. Review Zillow's Terms of Service before use.
