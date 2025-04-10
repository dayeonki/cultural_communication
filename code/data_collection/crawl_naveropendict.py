import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

output_file = "naver_opendict_ko.jsonl"

# Load existing scraped pages
scraped_pages = set()
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                if "page_num" in data:
                    scraped_pages.add(data["page_num"])
            except json.JSONDecodeError:
                continue  # Skip any malformed lines

page_num = 1

with open(output_file, "a", encoding="utf-8") as f:
    while True:
        if page_num in scraped_pages:
            print(f"Skipping already scraped page {page_num}...")
            page_num += 1
            continue  # Skip this page

        print(f"Scraping page {page_num}...")

        url = f"https://open-pro.dict.naver.com/_ivo/dictmain?dictID=opendict_ko&page={page_num}"
        driver.get(url)
        time.sleep(3)  # Wait for JavaScript content to load
        index = 1

        while True:
            try:
                entry = {"lang": "ko", "page_num": page_num}

                # Word
                word_xpath = f'//*[@id="content"]/div[2]/div[5]/div[2]/ul/div[{index}]/a/strong'
                word_element = driver.find_element(By.XPATH, word_xpath)
                entry["keyword"] = word_element.text.strip()

                # Description
                desc_xpath = f'//*[@id="content"]/div[2]/div[5]/div[2]/ul/div[{index}]/a/div[1]'
                desc_element = driver.find_element(By.XPATH, desc_xpath)
                entry["description"] = desc_element.text.strip()

                # Like
                like_xpath = f'//*[@id="content"]/div[2]/div[5]/div[2]/ul/div[{index}]/div/span[1]/span'
                like_element = driver.find_element(By.XPATH, like_xpath)
                entry["likes"] = like_element.text.strip()

                # Writer
                writer_xpath = f'//*[@id="content"]/div[2]/div[5]/div[2]/ul/div[{index}]/a/div[2]/span'
                writer_element = driver.find_element(By.XPATH, writer_xpath)
                entry["writer"] = writer_element.text.strip()

                # View
                view_xpath = f'//*[@id="content"]/div[2]/div[5]/div[2]/ul/div[{index}]/div/span[3]/span'
                view_element = driver.find_element(By.XPATH, view_xpath)
                entry["views"] = view_element.text.strip()

                # Date
                date_xpath = f'//*[@id="content"]/div[2]/div[5]/div[2]/ul/div[{index}]/div/span[4]'
                date_element = driver.find_element(By.XPATH, date_xpath)
                entry["date"] = date_element.text.strip()

                # Write entry to file immediately
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                f.flush()
                new_entries = True

                index += 1
            except:
                break  # Stop when no more elements are found

        page_num += 1  # Go to the next page

driver.quit()