from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://www.saucedemo.com/"
STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


def create_driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def login(driver, username=STANDARD_USER, password=PASSWORD):
    wait = WebDriverWait(driver, 10)

    driver.get(BASE_URL)

    wait.until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()


def test_happy_path_checkout():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        login(driver)

        wait.until(EC.url_contains("inventory"))
        assert "inventory" in driver.current_url

        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]')
            )
        ).click()

        cart_badge = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        assert cart_badge.text == "1"

        wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        ).click()

        wait.until(EC.url_contains("cart"))
        assert "Sauce Labs Backpack" in driver.page_source

        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test="checkout"]'))
        ).click()

        wait.until(EC.url_contains("checkout-step-one"))

        first_name = wait.until(EC.element_to_be_clickable((By.ID, "first-name")))
        first_name.click()
        first_name.send_keys("Jane")

        last_name = wait.until(EC.element_to_be_clickable((By.ID, "last-name")))
        last_name.click()
        last_name.send_keys("Tester")

        postal_code = wait.until(EC.element_to_be_clickable((By.ID, "postal-code")))
        postal_code.click()
        postal_code.send_keys("12345")

        wait.until(
            EC.element_to_be_clickable((By.ID, "continue"))
        ).click()

        wait.until(EC.url_contains("checkout-step-two"))
        assert "checkout-step-two" in driver.current_url

        finish_button = wait.until(EC.element_to_be_clickable((By.ID, "finish")))
        driver.execute_script("arguments[0].scrollIntoView(true);", finish_button)
        finish_button.click()

        complete_header = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        assert complete_header.is_displayed()
        assert complete_header.text == "Thank you for your order!"

    finally:
        driver.quit()


def test_invalid_login_shows_error():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        login(driver, username="locked_out_user", password=PASSWORD)

        error_box = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test="error"]'))
        )
        assert error_box.is_displayed()

    finally:
        driver.quit()


def test_checkout_missing_first_name():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        login(driver)

        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]')
            )
        ).click()

        wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        ).click()

        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test="checkout"]'))
        ).click()

        wait.until(EC.url_contains("checkout-step-one"))

        last_name = wait.until(EC.element_to_be_clickable((By.ID, "last-name")))
        last_name.click()
        last_name.send_keys("Tester")

        postal_code = wait.until(EC.element_to_be_clickable((By.ID, "postal-code")))
        postal_code.click()
        postal_code.send_keys("12345")

        wait.until(
            EC.element_to_be_clickable((By.ID, "continue"))
        ).click()

        error_box = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test="error"]'))
        )
        assert error_box.is_displayed()

    finally:
        driver.quit()


def test_remove_item_from_cart():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        login(driver)

        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]')
            )
        ).click()

        wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        ).click()

        cart_items = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item"))
        )
        assert len(cart_items) == 1

        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test="remove-sauce-labs-backpack"]')
            )
        ).click()

        wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "cart_item"))
        )

        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 0

    finally:
        driver.quit()