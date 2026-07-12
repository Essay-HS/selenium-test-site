import pytest       
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.smoke
def test_contact_page_loads(driver, base_url):
    driver.get(f"{base_url}/contact")

    contact_form = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(
            (By.ID, "contact-form")
        )
    )

    assert contact_form.is_displayed()
    assert driver.find_element(By.ID, "contact-name").is_displayed()
    assert driver.find_element(By.ID, "contact-email").is_displayed()
    assert driver.find_element(By.ID, "contact-subject").is_displayed()
    assert driver.find_element(By.ID, "contact-message").is_displayed()
    assert driver.find_element(By.ID, "contact-submit").is_displayed()


def test_contact_form_required_fields(driver, base_url):
    driver.get(f"{base_url}/contact")

    name_field = driver.find_element(By.ID, "contact-name")
    email_field = driver.find_element(By.ID, "contact-email")
    subject_field = driver.find_element(By.ID, "contact-subject")
    message_field = driver.find_element(By.ID, "contact-message")

    assert name_field.get_attribute("required") is not None
    assert email_field.get_attribute("required") is not None
    assert subject_field.get_attribute("required") is not None
    assert message_field.get_attribute("required") is not None


def test_contact_email_field_uses_email_type(driver, base_url):
    driver.get(f"{base_url}/contact")

    email_field = driver.find_element(By.ID, "contact-email")

    assert email_field.get_attribute("type") == "email"


def test_contact_field_length_limits(driver, base_url):
    driver.get(f"{base_url}/contact")

    subject_field = driver.find_element(By.ID, "contact-subject")
    message_field = driver.find_element(By.ID, "contact-message")

    assert subject_field.get_attribute("maxlength") == "200"
    assert message_field.get_attribute("maxlength") == "3000"


def test_invalid_contact_email_is_rejected(driver, base_url):
    driver.get(f"{base_url}/contact")

    driver.find_element(By.ID, "contact-name").send_keys("Test User")
    driver.find_element(By.ID, "contact-email").send_keys("invalid-email")
    driver.find_element(By.ID, "contact-subject").send_keys("Test Subject")
    driver.find_element(By.ID, "contact-message").send_keys("Test message")
    driver.find_element(By.ID, "contact-submit").click()

    email_field = driver.find_element(By.ID, "contact-email")

    assert email_field.get_attribute("validationMessage") != ""