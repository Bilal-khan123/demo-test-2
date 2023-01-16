# Problem Statement 1
'''
# Write a python code using web scraping method for creating a list of
1) Name of Diseases,
2) URLs associated with diseases and,
3) Icon images of diseases.
Save the list as a CSV file.
Create the folder using python commands to save the icon images.
URL of webpage: Dermnrtnz.org
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import time
import csv, io, os
from PIL import Image
import requests


def delay(wait_time = 0):
    time.sleep(3 + wait_time)

# chrome_options.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extension")
chrome_options.add_argument('--no-sandbox') # Bypass OS security model
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--incognito")


def download_image(url, file_name):     # function to download image
    try:
        image_content = requests.get(url).content           # get image content
        image_file = io.BytesIO(image_content)              # convert into bytes
        image = Image.open(image_file)                      # open image
        rgb_im = image.convert('RGB')                       # convert into RGB values
        file_path = 'icon image/' + file_name + '.jpeg'     # setting file path

        if not os.path.exists('icon image'):                # make icon image folder if not present
            os.makedirs('icon image')

        with open(file_path, "wb") as f:                    
            rgb_im.save(f, "JPEG")                          # save the image
        print("Sucess")
    
    except Exception as e:
        print('Failed -', e)

def main():
    # Driver
    try:
        ser = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=ser, options= chrome_options)        
    except WebDriverException:
        pass

    driver.get('https://dermnetnz.org/image-library')       # navigate to the given link
    delay()

    name_of_disease_path = driver.find_elements(By.XPATH, "//a[@class='imageList__group__item']/div[2]/h6")     # Name of the disease XPATH (list)

    links_with_disease_path = driver.find_elements(By.XPATH, "//a[@class='imageList__group__item']")            # links associated with names XPATH (list)

    disease_image_path = driver.find_elements(By.XPATH, "//a[@class='imageList__group__item']/div[1]/img")      # Image of diseases XPATH (links)

    filename = 'data.csv'
    # opening extracted data.csv file
    with open(f'{filename}', 'a', newline='\n') as file:
        fieldnames = ['Name of the disease', 'Link']
        writer_f = csv.DictWriter(file, fieldnames=fieldnames)
        writer_f.writeheader()

        i = 0
        while i in range(0, len(name_of_disease_path)):             # looping through the lists to save one by one  
            print(i+1)
            name_of_disease = name_of_disease_path[i].text
            links_with_disease = links_with_disease_path[i].get_attribute("href")
            disease_image_url = disease_image_path[i].get_attribute("src")

                # saving to data.csv
            writer_f.writerow({'Name of the disease': name_of_disease, 'Link': links_with_disease})   
                
                # downloading image
            download_image(disease_image_url, name_of_disease)
            i +=1

    print('finished.')
    driver.close()

if __name__ == '__main__':
    main()