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


def test_add_remove_elements():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://the-internet.herokuapp.com/add_remove_elements/")

        add_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']"))
        )
        add_button.click()
        add_button.click()
        add_button.click()

        delete_buttons = driver.find_elements(By.XPATH, "//button[text()='Delete']")
        assert len(delete_buttons) == 3

        delete_buttons[0].click()

        delete_buttons = driver.find_elements(By.XPATH, "//button[text()='Delete']")
        assert len(delete_buttons) == 2

    finally:
        driver.quit()


def test_add_remove_delete_all():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://the-internet.herokuapp.com/add_remove_elements/")

        add_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']"))
        )

        for _ in range(4):
            add_button.click()

        delete_buttons = driver.find_elements(By.XPATH, "//button[text()='Delete']")
        assert len(delete_buttons) == 4

        while len(driver.find_elements(By.XPATH, "//button[text()='Delete']")) > 0:
            driver.find_elements(By.XPATH, "//button[text()='Delete']")[0].click()

        delete_buttons = driver.find_elements(By.XPATH, "//button[text()='Delete']")
        assert len(delete_buttons) == 0

    finally:
        driver.quit()
