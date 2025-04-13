import os
import time
import json
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

input_path = 'naver_opendict_ko_official.jsonl'
output_path = 'naver_qa.jsonl'

# Load already processed words
processed_words = set()
if os.path.exists(output_path):
    with open(output_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                if 'word' in item:
                    processed_words.add(item['word'])
            except json.JSONDecodeError:
                continue

def get_actual_post_titles(word):
    search_url = f'https://kin.naver.com/search/list.naver?query={urllib.parse.quote(word)}'
    driver.get(search_url)
    time.sleep(2)

    titles = []
    for i in range(1, 6):
        try:
            link_xpath = f'//*[@id="s_content"]/div[3]/ul/li[{i}]/dl/dt/a'
            link_element = driver.find_element(By.XPATH, link_xpath)
            href = link_element.get_attribute('href')

            driver.execute_script("window.open(arguments[0]);", href)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)

            try:
                post_title_elem = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[1]')
                titles.append(post_title_elem.text.strip().replace("질문\n", ""))
            except Exception:
                titles.append('None')

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print(f'Could not find post {i} for word "{word}": {e}')
            pass
    return titles

# Open output file in append mode
with open(output_path, 'a', encoding='utf-8') as outfile:
    with open(input_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            entry = json.loads(line)
            word = entry.get('word')
            if not word:
                continue

            if word in processed_words:
                print(f"Skipping '{word}' (already processed)")
                continue

            try:
                actual_titles = get_actual_post_titles(word)
                print(f"Term: {word}")
                print(f"Examples: {actual_titles}")
                entry['kin_titles'] = actual_titles
            except Exception as e:
                print(f"Failed on word '{word}': {e}")
                entry['kin_titles'] = []

            outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')
            outfile.flush()
            processed_words.add(word)

driver.quit()
