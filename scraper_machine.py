from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


def scrape_and_save_offers(url):


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        # Accept cookie policy
        policy_accept = driver.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']")
        policy_accept.click()

        # Find elements containing single offer price, description, and link
        single_offer_price = driver.find_elements(By.CSS_SELECTOR,
                                                  "div[data-testid='listing-item-header'] span.e1a3ad6s0")
        second = driver.find_elements(By.CSS_SELECTOR, "p[data-testid='advert-card-address']")
        third = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='listing-item-link']")

        # Print lengths for debugging
        print(len(single_offer_price))
        print(len(second))
        print(len(third))

        if len(single_offer_price) > 0:
            # Prepare data for saving
            all_offers = {}
            for n in range(len(single_offer_price)):
                all_offers[n] = {
                    "name": single_offer_price[n].text,
                    "last": second[n].text,
                    "link": third[n].text,
                    "fourth": third[n].get_attribute("href")
                }

            # Convert to string
            str_to_save = str(all_offers)

            # Get the current date and time
            current_datetime = datetime.now()

            # Convert the datetime object to a string
            current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # Append the current date and time along with the data to save
            data_to_save = f"{current_datetime_str}: {str_to_save}"

            # Save to file
            with open("scraped/my_data.txt", mode="a") as file:
                file.write("\n" + data_to_save)
        else:
            print("No offers found.")
            driver.quit()
            scrape_and_save_offers(url)

    finally:
        # Close the WebDriver
        driver.quit()