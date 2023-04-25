from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By

booking_site_url = 'https://www.recreation.gov/venues/VR2828/details/kpf4lm06qvdb'
day_of_week = 'Wednesday, April 26, 2023'
res_time = '1300-1500'
login_email = 'megan@volosports.com'
login_password = 'Volo123!'

def handler(event=None, context=None):
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
    driver.get(booking_site_url)
    
    try:
        driver.get(booking_site_url)
        driver.find_element(By.CSS_SELECTOR, '.sarsa-day-picker-range-controller-month-navigation-button.right').click() 
        sleep(.5)
    except Exception as e:
        print(e)
        #return False
    finally:
	# close the drivers
        driver.quit()
    
    driver.get("https://example.com/")
    
    return driver.find_element(by=By.XPATH, value="//html").text
