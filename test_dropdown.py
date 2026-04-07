from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def create_driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def test_dropdown_select_option_1():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://the-internet.herokuapp.com/dropdown")

        dropdown_element = wait.until(
            EC.presence_of_element_located((By.ID, "dropdown"))
        )
        dropdown = Select(dropdown_element)

        dropdown.select_by_value("1")
        selected = dropdown.first_selected_option
        assert selected.text == "Option 1"

    finally:
        driver.quit()


def test_dropdown_switch_to_option_2():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://the-internet.herokuapp.com/dropdown")

        dropdown_element = wait.until(
            EC.presence_of_element_located((By.ID, "dropdown"))
        )
        dropdown = Select(dropdown_element)

        dropdown.select_by_value("1")
        assert dropdown.first_selected_option.text == "Option 1"

        dropdown.select_by_value("2")
        assert dropdown.first_selected_option.text == "Option 2"

    finally:
        driver.quit()