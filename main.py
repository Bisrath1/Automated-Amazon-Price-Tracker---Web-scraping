import requests
import random
import time
import logging
from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()]
)


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

# Function to fetch the page content
def fetch_page(url):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logging.info("Successfully fetched the page.")
        return response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the page: {e}")
        return None

# Function to parse the page and extract name and price
def extract_product_details(page_content):
    try:
        soup = BeautifulSoup(page_content, "lxml")
        product_name = soup.find(id="productTitle").get_text(strip=True)
        price = soup.find(class_="a-offscreen").get_text()
        price_without_currency = price.replace("$", "").replace(",", "")
        price_as_float = float(price_without_currency)
        logging.info(f"Extracted product name: {product_name}")
        logging.info(f"Extracted price: {price_as_float}")
        return product_name, price_as_float
    except AttributeError as e:
        logging.error(f"Error extracting product details: {e}")
        return None, None
    except ValueError as e:
        logging.error(f"Error converting price to float: {e}")
        return None, None

# Function to save product details to a file
def save_to_file(product_name, price):
    try:
        with open("product_details.txt", "a") as file:
            file.write(f"Product: {product_name}\nPrice: ${price:.2f}\n\n")
        logging.info("Product details saved to file.")
    except Exception as e:
        logging.error(f"Error saving product details to file: {e}")

# Function to implement rate limiting
def rate_limit(min_delay=2, max_delay=5):
    delay = random.uniform(min_delay, max_delay)
    logging.info(f"Sleeping for {delay:.2f} seconds to avoid detection.")
    time.sleep(delay)

# Main function to orchestrate the scraper
def main():
    url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
    page_content = fetch_page(url)

    if page_content:
        product_name, price = extract_product_details(page_content)
        if product_name and price is not None:
            print(f"The extracted product is: {product_name}")
            print(f"The extracted price is: ${price:.2f}")
            save_to_file(product_name, price)
        else:
            print("Failed to extract product details.")
    else:
        print("Failed to fetch the page.")


    rate_limit()

if __name__ == "__main__":
    main()