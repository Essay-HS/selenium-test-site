from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_delayed_message(driver, base_url):
    driver.get(base_url)

    delayed_button = driver.find_element(
        By.ID,
        "delayed-button",
    )

    delayed_button.click()

    wait = WebDriverWait(driver, 10)

    message_loaded = wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "delayed-message"),
            "The delayed message has loaded.",
        )
    )

    assert message_loaded is True

    message_element = driver.find_element(
        By.ID,
        "delayed-message",
    )

    assert message_element.text == (
        "The delayed message has loaded."
    )