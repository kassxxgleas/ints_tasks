from selenium import webdriver
import pytest


@pytest.fixture()
def driver():
    driver = webdriver.Edge() 
    driver.maximize_window()
    driver.implicitly_wait(3)
    yield driver
    # browser.close() for FireFox