# scrape_bbc

A Python-based web scraper for extracting data (e.g., headlines) from the BBC website. This project uses the `requests` library for HTTP requests, `BeautifulSoup` for parsing HTML, and `loguru` for logging.

---

## Features
- Scrapes data (e.g., headlines) from the BBC homepage.
- Saves the extracted data to a file (`data/headlines.txt`).
- Logs scraping activity to `logs/scraper.log`.
- Modular structure with configurable settings.

---

## Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- `pip` for managing Python packages
- `virtualenv` for creating isolated Python environments (optional but recommended)

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/reypkn/scrape_bbc.git
cd scrape_bbc
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
Create and activate a virtual environment to isolate dependencies:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Scraper

To run the scraper and extract data:
```bash
python main.py
```

### Output:
- Scraped data (e.g., headlines) will be saved to `data/headlines.txt`.
- Logs will be saved to `logs/scraper.log`.

---

## Project Structure

```
scrape_bbc/
├── main.py               # Entry point for the scraper
├── requirements.txt      # Project dependencies
├── .gitignore            # Ignored files and directories
├── data/                 # Directory for storing scraped data
├── logs/                 # Directory for storing log files
├── scraper/              # Scraper package
│   ├── scrape.py         # Main scraping logic
│   ├── config.py         # Configuration settings
│   └── utils.py          # Utility functions
└── tests/                # Directory for unit tests
```

---

## Configuration

You can modify the scraper's behavior by editing the `scraper/config.py` file:
- **`BBC_URL`**: The URL to scrape (default: `https://www.bbc.com`).
- **`REQUEST_TIMEOUT`**: HTTP request timeout in seconds.

---

## Logging

Logs are saved to `logs/scraper.log` and include:
- Info-level logs for scraping progress.
- Error-level logs for any issues encountered.

---

## Testing

This project uses `pytest` for unit testing. To run tests:
```bash
pytest
```

---

## Dependencies

The project uses the following Python libraries:
- `requests`: For making HTTP requests.
- `beautifulsoup4`: For parsing HTML content.
- `loguru`: For logging.

These are listed in the `requirements.txt` file.

---

## Future Enhancements

- Add support for scraping multiple pages.
- Implement data filtering and sorting.
- Save data in different formats (e.g., JSON, CSV).

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author

Developed by [reypkn](https://github.com/reypkn).