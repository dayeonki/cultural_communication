
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
# chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

output_file = "chinatogod_data.jsonl"


scraped_pages = set()
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                if "page_num" in data:
                    scraped_pages.add(data["page_num"])
            except json.JSONDecodeError:
                continue  # Skip malformed lines

start_page = 1
max_pages = 20


with open(output_file, "a", encoding="utf-8") as f:
    for page_num in range(start_page, max_pages + 1):
        if page_num in scraped_pages:
            print(f"Skipping already scraped page {page_num}...")
            continue  # Skip already scraped pages

        print(f"Scraping page {page_num}...")

        url = f"http://www.chinatogod.com/main/z2_search_.php?page={page_num}&si=0&all_search=%BD%C5%C1%B6%BE%EE%B7%CE"
        driver.get(url)
        time.sleep(3)

        tr_index = 2

        while True:
            try:
                link_xpath = f'/html/body/table[5]/tbody/tr[1]/td/table[2]/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr[5]/td/table/tbody/tr[{tr_index}]/td/a[2]'
                link_element = driver.find_element(By.XPATH, link_xpath)
                link_url = link_element.get_attribute("href")

                driver.execute_script("arguments[0].click();", link_element)
                time.sleep(3)

                entry = {"page_num": page_num, "row_index": tr_index, "url": link_url}

                # Title
                try:
                    title_element = driver.find_element(By.XPATH, "/html/body/table[5]/tbody/tr[1]/td/table[2]/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr[8]/td")
                    entry["title"] = title_element.text.strip()
                except:
                    entry["title"] = "N/A"

                # Content
                try:
                    content_element = driver.find_element(By.XPATH, "/html/body/table[5]/tbody/tr[1]/td/table[2]/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr[12]/td")
                    entry["content"] = content_element.text.strip()
                except:
                    entry["content"] = "N/A"
                
                print(entry)
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                f.flush()

                driver.back()
                time.sleep(2)

                tr_index += 2

            except:
                print(f"No more valid links on page {page_num}. Moving to next page...")
                break

driver.quit()