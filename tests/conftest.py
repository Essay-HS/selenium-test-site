import os
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


@pytest.fixture(scope="session")
def base_url():
    """
    Return the website address used by the entire test session.

    BASE_URL can point the tests to the public website.
    If BASE_URL is not supplied, the tests use the local site.
    """
    return os.getenv(
        "BASE_URL",
        "http://127.0.0.1:5000",
    ).rstrip("/")


@pytest.fixture(scope="session", autouse=True)
def wait_for_site(base_url):
    """
    Wait until the Flask website is ready before tests begin.

    The live Render site can take longer to start after inactivity.
    """
    is_live_site = not (
        "127.0.0.1" in base_url
        or "localhost" in base_url
    )

    maximum_wait = 180 if is_live_site else 30
    check_interval = 5
    deadline = time.time() + maximum_wait
    last_error = None

    print(f"\nChecking website availability: {base_url}")

    while time.time() < deadline:
        try:
            with urlopen(base_url, timeout=20) as response:
                page_html = response.read().decode(
                    "utf-8",
                    errors="ignore",
                )

                website_is_ready = (
                    response.status == 200
                    and 'id="page-title"' in page_html
                    and "Selley QA" in page_html
                )

                if website_is_ready:
                    print("Website is ready. Starting tests.\n")
                    return

                last_error = (
                    "The server responded, but the actual "
                    "homepage was not ready yet."
                )

        except (HTTPError, URLError, TimeoutError, OSError) as error:
            last_error = str(error)

        print(
            "Website is still starting. "
            f"Checking again in {check_interval} seconds..."
        )

        time.sleep(check_interval)

    pytest.fail(
        f"The website did not become ready within "
        f"{maximum_wait} seconds.\n"
        f"Address: {base_url}\n"
        f"Last result: {last_error}"
    )


@pytest.fixture
def driver():
    """
    Create a Firefox browser for each Selenium test.

    Set HEADLESS=true when the browser should run without appearing.
    """
    options = Options()

    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("-headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

    browser = webdriver.Firefox(options=options)

    yield browser

    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Save a browser screenshot when a Selenium test fails.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    driver = item.funcargs.get("driver")

    if driver is None:
        return

    screenshot_folder = Path("test-results/screenshots")
    screenshot_folder.mkdir(parents=True, exist_ok=True)

    safe_test_name = item.nodeid.replace("/", "_").replace("::", "__")
    safe_test_name = safe_test_name.replace("[", "_").replace("]", "")

    screenshot_path = screenshot_folder / f"{safe_test_name}.png"

    try:
        driver.save_screenshot(str(screenshot_path))
        print(f"\nFailure screenshot saved: {screenshot_path}")
    except Exception as error:
        print(f"\nCould not save failure screenshot: {error}")