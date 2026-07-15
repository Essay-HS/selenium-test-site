import pytest
from selenium.webdriver.common.by import By


@pytest.mark.smoke
@pytest.mark.regression
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


@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password",
    [
        ("testuser", "WrongPassword"),
        ("wronguser", "Password123"),
        ("wronguser", "WrongPassword"),
        ("TESTUSER", "Password123"),
        ("testuser", "password123"),
    ],
)
def test_invalid_login_attempts(
    driver,
    base_url,
    username,
    password,
):
    driver.get(f"{base_url}/login")

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    message = driver.find_element(By.ID, "login-message")

    assert message.text == "Invalid username or password"


@pytest.mark.regression
def test_password_field_hides_typed_text(driver, base_url):
    driver.get(f"{base_url}/login")

    password_field = driver.find_element(By.ID, "password")

    assert password_field.get_attribute("type") == "password"