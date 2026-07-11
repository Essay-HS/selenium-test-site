from selenium.webdriver.common.by import By


def test_successful_login(driver, base_url):
    driver.get(f"{base_url}/login")

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_field.send_keys("testuser")
    password_field.send_keys("Password123")
    login_button.click()

    message = driver.find_element(By.ID, "login-message")

    assert message.text == "Login successful"


def test_failed_login(driver, base_url):
    driver.get(f"{base_url}/login")

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_field.send_keys("testuser")
    password_field.send_keys("WrongPassword")
    login_button.click()

    message = driver.find_element(By.ID, "login-message")

    assert message.text == "Invalid username or password"