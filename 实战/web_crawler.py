from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import csv
import os

# Path to your WebDriver (e.g., ChromeDriver)
driver_path = '/usr/local/bin/chromedriver' # Change this to the path of your WebDriver

# Initialize the Chrome WebDriver using Service
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Define the base URL
base_url = 'https://s.taobao.com/search?commend=all&ie=utf8&initiative_id=tbindexz_20170306&q=%E5%A5%B6%E7%B2%89&search_type=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ssid=s5-e&tab=all&page={}'

# Initialize lists to store all products
all_products = []

# Get the current directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Loop through pages 1 to 10
for page_num in range(1, 4):
    # Construct the URL for the current page
    url = base_url.format(page_num)
    driver.get(url)
    
    # Wait for the products to load
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Card--doubleCard--wznk5U4"))
        )
    except Exception as e:
        print("Error: ", e)
        continue
    
    # Get the page source after it has fully loaded
    page_html = driver.page_source
    
     # Write the page HTML response to a file named pagenum_response.html
    html_file_path = os.path.join(script_directory, f'page{page_num}_response.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(page_html)
    
    print(f"Page {page_num} HTML saved to {html_file_path}")
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_html, 'html.parser')
    
    # Find all product containers
    product_containers = soup.find_all('div', class_='Card--doubleCard--wznk5U4')
    
    # Iterate over each product container
    for product_container in product_containers:
        # Initialize dictionary to store product details
        product_details = {}
        
        # Extract product details
        product_details['name'] = product_container.find('div', class_='Title--title--jCOPvpf').text.strip()
        product_details['currency'] = product_container.find('span', class_='Price--unit--VNGKLAP').text.strip()
        product_details['price'] = ''.join(filter(str.isdigit, product_container.find('span', class_='Price--priceInt--ZlsSi_M').text.strip())) + product_container.find('span', class_='Price--priceFloat--h2RR0RK').text.strip()
        product_details['sales'] = ''.join(filter(str.isdigit, product_container.find('span', class_='Price--realSales--FhTZc7U').text.strip()))
        product_details['location'] = product_container.find_all('div', class_='Price--procity--_7Vt3mX')[0].text.strip()
        product_details['store'] = product_container.find('a', class_='ShopInfo--shopName--rg6mGmy').text.strip()
        
        # Append product details to the list of all products
        all_products.append(product_details)


# Write all product details to a CSV file
csv_file_path = os.path.join(script_directory, 'result.csv')
with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['name', 'currency', 'price', 'sales', 'location', 'store']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for product in all_products:
        writer.writerow(product)

print("Data saved to result.csv")

# Close the WebDriver
driver.quit()
