from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
import csv
import time
import math

def chrome_proxy(user: str, password: str, endpoint: str) -> dict:
    wire_options = {
        "proxy": {
            "http": f"http://{user}:{password}@{endpoint}",
            "https": f"https://{user}:{password}@{endpoint}",
        }
    }
    return wire_options

def setup_driver_with_proxy_and_profile(proxy_host, proxy_port, username, password):
    manage_driver = Service(executable_path=ChromeDriverManager().install())
    proxies = chrome_proxy(username, password, f'{proxy_host}:{proxy_port}')
    
    driver = webdriver.Chrome(service=manage_driver, seleniumwire_options=proxies)
    return driver

def scrape_zillow_agents_selenium(zipcode, page, first_page):
    proxy_host = 'us-pr.oxylabs.io'
    proxy_port = 10000
    username = 'agentsmetrics_PfPKx'
    password = 'pw2chW8MqZfSigbA_'

    driver = setup_driver_with_proxy_and_profile(proxy_host, proxy_port, username, password)
    
    url = f"https://www.zillow.com/professionals/real-estate-agent-reviews/{zipcode}/?page={page}"
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    
    all_agents = []
    total_pages = 0
    
    try:
        if page == first_page:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Text-c11n-8-101-3__sc-aiai24-0"))
            )
            total_agents_text = driver.find_element(By.CSS_SELECTOR, "span.Text-c11n-8-101-3__sc-aiai24-0").text
            total_agents = int(total_agents_text.split()[0])
        
            agents_per_page = 16
            total_pages = math.ceil(total_agents / agents_per_page)
            print(f"Total agents: {total_agents}, Total pages: {total_pages}")
        
    except Exception as e:
        print(f"Error extracting total agents or pages: {e}")
        driver.quit()
        return [], 0

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "Grid-c11n-8-101-3__sc-18zzowe-0"))
        )
    except Exception as e:
        print(f"No more data on page {page}. Ending scrape.")
        driver.quit()
        return [], 0

    agents = driver.find_elements(By.CLASS_NAME, "Grid-c11n-8-101-3__sc-18zzowe-0.iZzmpw")
    if not agents:
        print(f"No agents found on page {page}. Ending scrape.")
        driver.quit()
        return [], 0

    for agent in agents:
        try:
            url = agent.find_element(By.TAG_NAME, "a").get_attribute('href')
        except:
            url = None
        
        all_agents.append({"URL": url})

    print(f"Scraped page {page} successfully.")
    driver.quit()
    return all_agents, total_pages

def save_to_csv(agent_data, filename="agents.csv"):
    if agent_data:
        with open(filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=agent_data[0].keys())
            writer.writerows(agent_data)
        print(f"Data saved to '{filename}'.")
    else:
        print(f"No data to save.")

def scrape_all_pages(zipcode, first_page):
    all_agents = []
    
    first_page = int(first_page)
    
    agents, total_pages = scrape_zillow_agents_selenium(zipcode, first_page, first_page)
    all_agents.extend(agents)
    save_to_csv(agents, filename=f"agents_{zipcode}.csv")
    print(f"Finished scraping page {first_page}.")
    
    if total_pages > 1:
        for page in range(first_page + 1, total_pages + 1):
            agents, _ = scrape_zillow_agents_selenium(zipcode, page, first_page)
            all_agents.extend(agents)
            save_to_csv(agents, filename=f"agents_{zipcode}.csv")
            print(f"Finished scraping page {page}.")

    print(f"{len(all_agents)} agents are scraped successfully.")
    
if __name__ == "__main__":
    zipcode = input("Enter the postal code: ").strip()
    first_page = input("Enter the first page: ").strip()
    scrape_all_pages(zipcode, first_page)
