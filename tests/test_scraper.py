import pytest
from scraper.scrape import BBCScraper

def test_scraper_initialization():
    scraper = BBCScraper()
    assert scraper.url == "https://www.bbc.com"

def test_scraper_response(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass
        text = "<html><h3>Headline 1</h3><h3>Headline 2</h3></html>"

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    scraper = BBCScraper()
    data = scraper.scrape()
    assert "Headline 1" in data
    assert "Headline 2" in data