from selenium.webdriver.common.by import By
import time # isn't good for auto tests


def test_open_s6(driver):
    driver.get('https://www.demoblaze.com/')
    galaxy_s6 = driver.find_element(By.XPATH, '//a[text() = "Samsung galaxy s6"]') # XPATH
    galaxy_s6.click()
    title = driver.find_element(By.CSS_SELECTOR, 'h2')
    assert title.text == 'Samsung galaxy s6' # pytest T_E/test_site.py


def test_two_monitors(driver):
    driver.get('https://www.demoblaze.com/')
    monitor_link = driver.find_element(By.CSS_SELECTOR, '''[onclick = "ByCat('monitor')"]''')
    monitor_link.click()
    time.sleep(2) # must be waiting for something happend
    monitors = driver.find_elements(By.CSS_SELECTOR, '.card')
    assert len(monitors) == 2