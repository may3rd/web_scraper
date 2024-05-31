from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import re

count:int = 0
ids:list = []

#chrome_binary_path = '\Applications\Google Chrome for Testing'
chrome_options = Options()
#chrome_options.binary_location = chrome_binary_path

service = Service(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to load a page with timeout handling
def load_page_with_retries(driver, url, timeout=10, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            driver.get(url)
            # Wait for a specific element to ensure the page has loaded
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            #print("Page loaded successfully")
            return True
        except TimeoutException:
            print(f"Timeout occurred. Retrying... ({retries + 1}/{max_retries})")
        except WebDriverException as e:
            print(f"WebDriverException occurred: {e}. Retrying... ({retries + 1}/{max_retries})")
        
        driver.refresh()
        retries += 1
    print("Failed to load the page after several retries")
    # Optionally, you can raise an exception or handle the failure case as needed

    return False


def scrape_pages(id, driver, file):

    global count

    # Open link in a new tab
    if load_page_with_retries(driver, 'https://esupport.aspentech.com/S_Article?id='+id):

        # Find all div elements with class "sfdc_richtext"
        div_elements = driver.find_elements(By.XPATH, "//div[@class='sfdc_richtext']")

        for div_element in div_elements:
            # Extract text content of each div element
            div_text = div_element.text

            # Print the extracted text
            print(count)
            count += 1

            # Write text to file
            file.write("-----------------------------------------------------------------------------------------------------\nID: " + id + "\n\n")
            file.write(div_text + "\n")
    else:
        print(id + ' not load.')


def go_to_next_page(driver):
    try:
        # Find and click the next page button
        next_button = driver.find_element(By.CLASS_NAME, "next__link")  # Change the locator as necessary
        
        if not next_button:
            return False
        
        next_button.click()
        time.sleep(2)
        return True
    except:
        return False

def save_list_to_file(my_list, filename):
    with open(filename, 'w') as file:
        for item in my_list:
            file.write(f"{item}\n")

def load_list_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]
    

def get_ids_list(driver, search_text=''):
    
    ids:list = []

    driver.get('https://explore.aspentech.com/?query=' + search_text)

    driver.implicitly_wait(10)

    div_element = driver.find_element(By.XPATH, "//div[@class='c-search__count']")

    count_text = div_element.text

    count_match = re.search(r'\b\d+\d', count_text)

    id_count = int(count_match.group())

    # Loop through pages and scrape data
    while True:
        #scrape_page(file)
        links = driver.find_elements(By.CSS_SELECTOR, "a.c-item__headline")

        for link in links:
            href_text = link.get_attribute('href')

            id_match = re.search(r"\b\d{9}\b", href_text)

            if id_match:
                ids.append(id_match.group())

        print(len(ids))

        if len(ids) >= id_count:
            break

        if not go_to_next_page():
            break

    return ids


def process_chunk(chunk, file):
    # Placeholder function to process each chunk
    # Replace with your actual processing logic
    print(f"Processing chunk of size {len(chunk)}")
    # Example processing: print the first item of each chunk
    
    driver_load = webdriver.Chrome(service=service, options=chrome_options)
    login_aspen(driver_load)

    for id in chunk:
        scrape_pages(id, driver_load, file)

    driver_load.quit()

def process_list_in_chunks(my_list, chunk_size, file):
    for i in range(0, len(my_list), chunk_size):
        chunk = my_list[i:i + chunk_size]
        process_chunk(chunk, file)


def login_aspen(driver):
    driver.get('https://esupport.aspentech.com/')

    login_btn = driver.find_element(by=By.NAME, value='j_id0:theForm:j_id33')
    login_btn.click()
    driver.implicitly_wait(5)

    username_box = driver.find_element(by=By.NAME, value='j_id0:theForm:userName')
    password_box = driver.find_element(by=By.NAME, value='j_id0:theForm:password')

    username_box.send_keys('maetee.lorprajuksiri@atcommunity.com')
    password_box.send_keys('oZXJTHfqeZjxN5j')
    password_box.send_keys(Keys.RETURN)

    driver.implicitly_wait(5)


load_ids = load_list_from_file('kb_ids.txt')


with open("output.txt", "a", encoding="utf-8") as file:
    chunk_size = 500

    process_list_in_chunks(load_ids, chunk_size, file)

