import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

@pytest.mark.smoke
def test_form_submission(driver, base_url):
    driver.get(f"{base_url}/form")

    name_field = driver.find_element(By.ID, "name")
    email_field = driver.find_element(By.ID, "email")
    role_dropdown = driver.find_element(By.ID, "role")
    advanced_radio = driver.find_element(By.ID, "advanced")
    newsletter_checkbox = driver.find_element(By.ID, "newsletter")
    submit_button = driver.find_element(By.ID, "submit-button")

    name_field.send_keys("Selley Spruell")
    email_field.send_keys("ss@selley.us")

    role_select = Select(role_dropdown)
    role_select.select_by_visible_text("QA Analyst")

    advanced_radio.click()
    newsletter_checkbox.click()
    submit_button.click()

    result_name = driver.find_element(By.ID, "result-name")
    result_email = driver.find_element(By.ID, "result-email")
    result_role = driver.find_element(By.ID, "result-role")
    result_experience = driver.find_element(
        By.ID,
        "result-experience",
    )
    result_newsletter = driver.find_element(
        By.ID,
        "result-newsletter",
    )

    assert result_name.text == "Selley Spruell"
    assert result_email.text == "ss@selley.us"
    assert result_role.text == "QA Analyst"
    assert result_experience.text == "Advanced"
    assert result_newsletter.text == "Yes"