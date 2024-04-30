import csv
import os.path

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_and_save_offers(url, csv_file_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        # Accept cookie policy
        policy_accept = driver.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']")
        policy_accept.click()

        # Find elements containing single offer price, description, and link
        prices = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='listing-item-header'] span.e1a3ad6s0")
        streets = driver.find_elements(By.CSS_SELECTOR, "p[data-testid='advert-card-address']")
        descs = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='listing-item-link']")

        # Print lengths for debugging
        print(len(prices))
        print(len(streets))
        print(len(descs))

        if len(prices) > 0:
            # Prepare data for saving
            all_offers = []
            current_datetime = datetime.now()
            current_datetime_str = current_datetime.strftime("%Y-%m-%d")
            for price, street, desc in zip(prices, streets, descs):
                offer = {
                    "scraped_date": current_datetime_str,
                    "price": price.text,
                    "street": street.text,
                    "desc": desc.text,
                    "link": desc.get_attribute("href"),
                }
                all_offers.append(offer)

            # Define column names
            fieldnames = ["scraped_date", "price", "street", "desc", "link"]

            # Check if CSV file exists
            file_exists = os.path.isfile(csv_file_path)

            # Save data to CSV file
            with open(csv_file_path, mode="a", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader() 
                writer.writerows(all_offers)

            print(f"Data appended to: {csv_file_path}")
        else:
            print("No offers found.")
            driver.quit()
            scrape_and_save_offers(url, csv_file_path)

    finally:
        # Close the WebDriver
        driver.quit()


