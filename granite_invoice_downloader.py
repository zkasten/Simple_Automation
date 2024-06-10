from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
import time
import re
import datetime
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('credential.conf')
ID = config['GRANITE']['ID']
PW = config['GRANITE']['PW']

def main(args):
    driver = webdriver.Chrome()
    
    driver.get("https://rockreports.granitenet.com/billing")
    title = driver.title
    assert title == "Rock Reports"
    
    driver.implicitly_wait(0.5)

    id = ID
    pw = PW
    driver.find_element(by=By.NAME, value="UserName").send_keys(id)
    driver.find_element(by=By.NAME, value="Password").send_keys(pw)

    login_btn = driver.find_element(by=By.XPATH, value='//button[@class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--raised mdl-button--colored"]')
    login_btn.click()

    driver.implicitly_wait(10)
    search_option = driver.find_element(by=By.XPATH, value='//mat-panel-title[@class="mat-expansion-panel-header-title ng-tns-c213-3"]')
    search_option.click()

    last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    start_date = last_month.strftime("%m/%d/%Y")

    driver.implicitly_wait(0.5)
    from_date = driver.find_element(by=By.ID, value='mat-input-4')
    length = len(from_date.get_attribute('value'))
    from_date.send_keys(length * Keys.BACKSPACE)
    from_date.send_keys(start_date)

    driver.find_element(by=By.NAME, value='pastDue').click()
    
    while True:
        try:
            searching = driver.find_element(by=By.CSS_SELECTOR, value='granite-loading.ng-star-inserted').get_attribute('message')

            if searching:
                #print("SEARCHING"+ searching)
                time.sleep(0.5)
            
        except Exception as e:
            break

    print("search")
    driver.implicitly_wait(0.5)
    driver.find_element(by=By.XPATH, value='//*[@id="cdk-accordion-child-0"]/div/form/div/div[4]/div/button[1]').click()

    while True:
        try:
            searching = driver.find_element(by=By.CSS_SELECTOR, value='granite-loading.ng-star-inserted').get_attribute('message')

            if searching:
                #print("SEARCHING"+ searching)
                time.sleep(0.5)
            
        except Exception as e:
            break

    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            while True:
                try:
                    searching = driver.find_element(by=By.CSS_SELECTOR, value='granite-loading.ng-star-inserted').get_attribute('message')

                    if searching:
                        #print("LOADING "+ searching)
                        time.sleep(0.5)
                except Exception as e:
                    break

            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(0.5)
            driver.find_element(by=By.CSS_SELECTOR, value='.btn.btn-primary.bs4.ng-star-inserted').click()
            print("show more")
        except Exception as e:
            break


    result = driver.find_element(by=By.XPATH, value='//*[@id="pcoded"]/div[2]/div/div/div/div/div/div/div/ng-component/ng-component/div[3]/div[2]/div/div[1]/div[1]/h2')
    print(result.accessible_name)

    driver.execute_script("window.scrollTo(0, 0);")
    driver.find_element(by=By.XPATH, value='//*[@id="pcoded"]/div[2]/div/div/div/div/div/div/div/ng-component/ng-component/div[3]/div[2]/div/table/thead/tr/th[1]/button').click()

    print('------ Download Invoices -------')
    inv_tbl = driver.find_element(by=By.XPATH, value='//*[@id="pcoded"]/div[2]/div/div/div/div/div/div/div/ng-component/ng-component/div[3]/div[2]/div/table')
    elements = inv_tbl.find_elements(by=By.TAG_NAME, value="a")
    inv_ptn = '^https.+invnum=\\d+$'

    for element in elements:
        link_url = element.get_attribute("href")
        inv_link = re.findall(inv_ptn, link_url)

        if inv_link:
            print(inv_link)
            element.click()

            desired_y = element.location['y'] - element.size['height'] *2
            driver.execute_script("window.scrollTo(0, arguments[0])", desired_y)
            print(element.size['height'])
            print(desired_y)

    time.sleep(60)
    driver.quit()


main(sys.argv[1:])
