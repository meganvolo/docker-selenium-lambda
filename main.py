from selenium import webdriver
from tempfile import mkdtemp
from time import sleep
from selenium.webdriver.common.by import By
import json

#booking_site_url = 'https://www.recreation.gov/venues/VR2828/details/kpf4lm06qvdb'
#day_of_week = 'Wednesday, May 3, 2023'
#res_time = '1300-1500'
#login_email = 'megan@volosports.com'
#login_password = 'Volo123!'

def handler(event=None, context=None):

    #params = json.loads(event)


    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome("/opt/chromedriver",
                              options=options)
    '''
    Select correct month
    '''
    driver.get(event["booking_site_url"])
    driver.find_element(By.CSS_SELECTOR, '.sarsa-day-picker-range-controller-month-navigation-button.right').click() 
    sleep(.5)

    '''
    Select correct day
    '''
    calendar_days = driver.find_elements(By.CLASS_NAME, 'CalendarDay')
    for day in calendar_days: 
        if(day.get_attribute('aria-label') == event["day_of_week"]):     
            day.click()

    '''
    Select correct time
    '''
    times_block = driver.find_elements(By.CLASS_NAME, 'venue-reservation-radio-pill')
    for time_block in times_block:
            times = time_block.find_elements(By.XPATH, './div')[2].find_elements(By.XPATH, './div/div/label')
            for time in times:
                try:
                    timeInput = time.find_element(By.XPATH, './/input')
                    value = timeInput.get_attribute('value')
                    if(value == event["res_time"]):
                        time.click()          
                except Exception as e:
                    continue  

    '''
        Login to account
        '''
    driver.find_element(By.ID, 'email').send_keys(event["login_email"])
    driver.find_element(By.ID, 'rec-acct-sign-in-password').send_keys(event["login_password"])
    buttons = driver.find_elements(By.CSS_SELECTOR, '.sarsa-button.sarsa-button-primary')
    for button in buttons: 
            if(button.get_attribute('aria-label') == 'Log In'):
                button.click()
                break

                    
    '''
        Add group size 50
        '''
    driver.find_element(By.ID, 'group_size').send_keys('50')

    '''
        Submit form
        '''
    button = driver.find_element(By.CSS_SELECTOR, '.sarsa-button.sarsa-button-primary')
    button.click()
    sleep(.5)

    '''
        Freeze to view (comment out when live)
        '''        
    sleep(1)  
    return event
