#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate

echo "Running the scraper..."
python main.py

echo "Deactivating virtual environment..."
deactivate