from selenium import webdriver
import pytest
from selenium.webdriver.edge.options import Options


@pytest.fixture()
def driver():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Edge(options = options) 
    driver.maximize_window()
    driver.implicitly_wait(3)
    yield driver
    # browser.close() for FireFox

# CSS SELECTOR
# #ID
# .class_name
# tag
# [atribute_name] ---> [atribute_name*="idde"] searching by start letters
# [atribute_name*="idde"] searching by sequence
# [atribute_name^="hidd"] searching by start letters
# [atribute_name$="idden"] searching by end letters
# tag.class_name or tag[atribute_name = "lalala"]
# [class ~= "requiredField"] # find by one of the attribute values
# we can find the element inside the parent element #div_id_text_string input(inside of div)
# form[method='post'] _  all elements in 
# form[method='post'] > element exactly in element 
# form[method='post'] ~ all elements after element 
# form[method='post'] + one element after element 
