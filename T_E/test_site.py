from selenium.webdriver.common.by import By
import time # isn't good for auto tests
from homepage import HomePage
from product import ProductPage

def test_open_s6(driver):
    homepage = HomePage(driver)
    homepage.open()
    homepage.click_galaxy_s6()
    product_page = ProductPage(driver)
    product_page.check_title_is('Samsing galaxy s6')


def test_two_monitors(driver):
    homepage = HomePage(driver)
    homepage.open()
    homepage.click_monitor()
    time.sleep(2) # must be waiting for something happend
    homepage.check_products_count(2)