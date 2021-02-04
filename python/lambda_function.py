from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import urllib3
import json
http = urllib3.PoolManager()

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1200x900')
    options.add_argument('--user-data-dir=/tmp/user-data')
    options.add_argument('--hide-scrollbars')
    #options.add_argument('--enable-logging')
    #options.add_argument('--log-level=0')
    #options.add_argument('--v=99')
    options.add_argument('--single-process')
    options.add_argument('--data-path=/tmp/data-path')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--homedir=/tmp')
    options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    options.binary_location = "/opt/python/bin/headless-chromium"

    driver = webdriver.Chrome('/opt/python/bin/chromedriver', options=options)
    return driver
    
def lambda_handler(event, context):
    driver = get_driver()
    # login
    driver.get('https://tmax.ezwel.com/cuser/login/loginForm.ez?clientCd=tmax')
    driver.find_element_by_id('loginSearchBean_userId').send_keys('2017119')
    driver.find_element_by_id('loginSearchBean_password1').send_keys(event['pass'])
    try:
        driver.find_element_by_class_name('lgn_ip_lgn').click() 
    except NoSuchElementException:
        pass

    driver.get('http://tmax.ezwel.com/family/anniversaryGiftMain_defer.ez?prmCd=10029285')
    cont_txt_elements = driver.find_elements_by_class_name('cont_txt')
    res = ""
    for element in cont_txt_elements:
        if "PTFE" in element.text:
            if "품절" in element.text:
                res = "Sold out"
            else:
                res = "Available"
            break
    
    # slack webhook noti
    url=event['url']
    msg = {
        "text": res,
    }
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg)
    driver.close()
    return res
