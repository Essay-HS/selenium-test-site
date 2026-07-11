from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_submissions_page_direct_access(driver, base_url):
    driver.get(f"{base_url}/submissions")

    heading = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "submissions-heading")
        )
    )

    assert heading.text == "Saved form submissions"


def test_submitted_record_appears_masked(driver, base_url):
    unique_value = uuid4().hex[:8]

    test_name = f"Submission {unique_value}"
    test_email = f"submission.{unique_value}@example.com"

    driver.get(f"{base_url}/form")

    name_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "name")
        )
    )

    email_field = driver.find_element(By.ID, "email")
    role_dropdown = driver.find_element(By.ID, "role")
    advanced_radio = driver.find_element(
        By.CSS_SELECTOR,
        'input[name="experience"][value="Advanced"]',
    )
    newsletter_checkbox = driver.find_element(
        By.ID,
        "newsletter",
    )
    submit_button = driver.find_element(
        By.CSS_SELECTOR,
        'button[type="submit"]',
    )

    name_field.send_keys(test_name)
    email_field.send_keys(test_email)

    role_dropdown.send_keys("QA Analyst")
    advanced_radio.click()
    newsletter_checkbox.click()
    submit_button.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "result-name")
        )
    )

    driver.get(f"{base_url}/submissions")

    submissions_table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "submissions-table")
        )
    )

    table_text = submissions_table.text

    # The full personal values should not appear publicly.
    assert test_name not in table_text
    assert test_email not in table_text

    # The masked values should still leave enough information
    # to recognize that a record exists.
    assert "S" in table_text
    assert "@e" in table_text