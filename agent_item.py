import csv
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

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
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    
    driver = webdriver.Chrome(service=manage_driver, options=options, seleniumwire_options=proxies)
    return driver

def scrape_agent_profile(url):
    proxy_host = 'us-pr.oxylabs.io'
    proxy_port = 10000
    username = 'agentsmetrics_PfPKx'
    password = 'pw2chW8MqZfSigbA_'

    driver = setup_driver_with_proxy_and_profile(proxy_host, proxy_port, username, password)
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    data = {
        "Headshot URL": "N/A",
        "Average Sales": "N/A",
        "Total Sales": "N/A",
        "Rents": "N/A",
        "Average Rent": "N/A",
        "License Number": "N/A",
    }
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        headshot = soup.select_one("img.Image-c11n-8-107-0__sc-1rtmhsc-0")
        data["Headshot URL"] = headshot["src"] if headshot else None

        stats = soup.select("div.Flex-c11n-8-107-0__sc-n94bjd-0.bXVNIZ")
        for stat in stats:
            label = stat.select_one("span.Text-c11n-8-107-0__sc-aiai24-0.gOSOFV")
            value = stat.select_one("span.Text-c11n-8-107-0__sc-aiai24-0.kUNVWz")
            if label and value:
                label_text = label.get_text(strip=True)
                value_text = value.get_text(strip=True)
                if label_text == "sales last 12 months":
                    data["Average Sales"] = value_text
                elif label_text == "total sales":
                    data["Total Sales"] = value_text
                elif label_text == "price range":
                    data["Rents"] = value_text
                elif label_text == "average price":
                    data["Average Rent"] = value_text
                elif label_text == "license number":
                    data["License Number"] = value_text

    except Exception as e:
        print(f"Error scraping profile: {e}")

    try:
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.StyledTextButton-c11n-8-107-0__sc-1nwmfqo-0.ezHcPX"))
        )
        
        for button in buttons:
            if button.text.strip() == "See license information":
                try:
                    license_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(button)
                    )
                    actions = ActionChains(driver)
                    actions.move_to_element(license_button).perform()
                    license_button.click()

                    license_modal = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, "section.StyledDialog-c11n-8-107-0__sc-11wyxbm-0.FWZwc")
                        )
                    )

                    license_number = license_modal.find_element(By.CSS_SELECTOR, "span.Text-c11n-8-107-0__sc-aiai24-0.kUNVWz").text
                    data["License Number"] = license_number
                    break  
                except Exception as e:
                    print(f"Error clicking license button: {e}")
                    continue  
            
    except Exception as e:
        print(f"Error: {e}")

    driver.quit()
    return data

def save_to_csv(data, filename="agents_data.csv"):
    """ Save the agent data to a CSV file """
    with open(filename, mode="a", newline="") as file:
        fieldnames = data.keys()  
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file.tell() == 0: 
            writer.writeheader()
        
        writer.writerow(data)
    print(f"Data saved to '{filename}'.")

def read_urls_from_csv(input_filename):
    """ Read URLs from a CSV file and return them as a list """
    urls = []
    with open(input_filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  
                urls.append(row[0])
    return urls

def scrape_agents_from_csv(input_filename):
    urls = read_urls_from_csv(input_filename)

    for url in urls:
        print(f"Scraping profile for {url}...")
        agent_data = scrape_agent_profile(url)
        save_to_csv(agent_data, filename="agents_data.csv")

if __name__ == "__main__":
    input_filename = input("Enter the CSV filename including urls: ").strip() + ".csv"
    scrape_agents_from_csv(input_filename)
