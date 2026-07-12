import pytest
from uuid import uuid4

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

@pytest.mark.smoke
def test_submissions_page_direct_access(driver, base_url):
    submissions_url = f"{base_url}/submissions"
    heading = None

    for attempt in range(3):
        driver.get(submissions_url)

        try:
            heading = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.ID, "submissions-heading")
                )
            )
            break
        except TimeoutException:
            if attempt == 2:
                raise

    assert heading is not None
    assert heading.text == "Saved form submissions"
    assert driver.current_url.rstrip("/") == submissions_url.rstrip("/")


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

    # Build the exact masked name that the website should display.
    expected_masked_name = " ".join(
        word[0] + "*" * (len(word) - 1)
        for word in test_name.split()
    )

    email_username, email_domain = test_email.split("@", 1)
    domain_name, domain_extension = email_domain.split(".", 1)

    expected_masked_email = (
        email_username[0]
        + "*" * (len(email_username) - 1)
        + "@"
        + domain_name[0]
        + "*" * (len(domain_name) - 1)
        + "."
        + domain_extension
    )

    # Private values must never appear on the public page.
    assert test_name not in table_text
    assert test_email not in table_text

    # The exact masked versions must appear.
    assert expected_masked_name in table_text
    assert expected_masked_email in table_text