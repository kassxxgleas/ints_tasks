from selenium import webdriver
import pytest
from selenium.webdriver.edge.options import Options


@pytest.fixture()
def driver():
    driver = webdriver.Edge() 
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


# XPATH LANGUAGE FOR SEARCHING HTML ELEMENTS
# //li[]
# @class ="bububu" @ before atribute for XPath
# //*[] - любой тег с нужным класом например
# //li[@class="tab"][1] - index якщо елементі пару а ми хочемо саме якиїсь
# //li[contains(@class, "tab")] - по частичному сходству
# //*[text() = "Simple Button"] - по тексту между тегами
# //label[@class="form-check-label" and contains(text() = "BububuBebebe")] оператор И, логический
# //a[starts-with(text(), "JD")]
# //a[starts-with(text(), "JD")]/following::input[] после елемента след 
# /child::tag поиск именно после елемента, в не ввложеных елементах
# /descendant::tag находим во всех елементах дочерних вложеных
# /ancestor::tag папу ищем дедушку и так далее
# /parent::tag отца оpдного сразу выше первого
