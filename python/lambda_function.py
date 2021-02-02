from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = "/opt/python/bin/headless-chromium"

    driver = webdriver.Chrome('/opt/python/bin/chromedriver', chrome_options=chrome_options)
    return driver
    
def lambda_handler(event, context):
    driver = get_driver()
    driver.get('https://talk.tmaxsoft.com')
    driver.find_element_by_name('id').send_keys('kwanghun_choi')
    driver.find_element_by_name('pass').send_keys('----')
    driver.find_element_by_id('loginPage_btn').click()
    
    driver.get('https://talk.tmaxsoft.com/front/bbs/findBoardList.do?boardKind=BBS20140826008&bbsGroupCd=TM0007&curPageBbsDiv=TOTAL&menuLevel=2&srchMenuNo=TM0007&toggleMenuNo=TM0012&')
    try:
        is_new = driver.find_element_by_css_selector("img[src='/images/new_icon.png']")
        is_new.click()
        src=driver.find_element_by_xpath("//*[contains(@src,'https://talk.tmaxsoft.com/upload/editor/x/')]").get_attribute('src')
        page_data = driver.page_source
    except NoSuchElementException:
        page_data = "Not found!"
    driver.close()
    
    return page_data
