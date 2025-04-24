import os

def save_data(data, file_path="data/scraped_data.html"):
    # Ensure the data folder exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save scraped data to a file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)
    print(f"Data saved to {file_path}")