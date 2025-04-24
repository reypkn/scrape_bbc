# Install dependencies
install:
	pip install -r requirements.txt

# Run the scraper
run:
	python main.py

# Run tests
test:
	pytest

# Clean up logs and data
clean:
	rm -rf logs/* data/*