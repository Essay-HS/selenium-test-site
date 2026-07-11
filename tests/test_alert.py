from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_javascript_alert(driver, base_url):
    driver.get(base_url)

    alert_button = driver.find_element(
        By.ID,
        "alert-button",
    )

    alert_button.click()

    wait = WebDriverWait(driver, 10)
    alert = wait.until(EC.alert_is_present())

    assert alert.text == "This is a Selenium practice alert."

    alert.accept()

    result_message = driver.find_element(
        By.ID,
        "alert-result",
    )

    assert result_message.text == "The alert was displayed."