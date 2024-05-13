from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Webdriver
browser = webdriver.Edge()

browser.get('https://en.wikipedia.org/wiki/Lists_of_stars')

time.sleep(5)

star_data = []

def scrape():
    global browser

    # BeautifulSoup Object
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # Loop to find elements using CSS selector
    for tr_tag in soup.select("table.wikitable tr:not(:first-child)"):
        td_tags = tr_tag.find_all("td")

        temp_list = []

        for td_tag in td_tags:
            temp_list.append(td_tag.text.strip())

        if temp_list:
            star_data.append(temp_list)

    # Find the "next page" button and click to move to the next page
    try:
        next_page_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "brightest-stars/page/2")]'))
        ).click()
        time.sleep(5)
        scrape()
    except:
        pass

# Calling Method
scrape()

# Define Header
headers = ["Name", "Distance (light-years)", "Mass (solar masses)", "Radius (solar radii)"]

# Define pandas DataFrame
star_df = pd.DataFrame(star_data, columns=headers)

# Print the content of the DataFrame
print(f'{"Name":<20} {"Distance (light-years)":<20} {"Mass (solar masses)":<20} {"Radius (solar radii)":<20}')
for index, row in star_df.iterrows():
    print(f'{row["Name"]:<20} {row["Distance (light-years)"]:<20.2f} {row["Mass (solar masses)"]:<20.4f} {row["Radius (solar radii)"]:<20.4f}')

# Convert to CSV
star_df.to_csv('brightest_stars.csv', index=False)