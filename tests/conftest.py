import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def base_url():
    """
    Return the website address used by the entire test session.

    The BASE_URL environment variable can point the tests to the
    public website. If it is not supplied, tests use the local site.
    """
    return os.getenv(
        "BASE_URL",
        "http://127.0.0.1:5000",
    ).rstrip("/")


@pytest.fixture(scope="session", autouse=True)
def wait_for_site(base_url):
    """
    Wait for the real Flask homepage before starting Selenium tests.

    This handles Render's cold-start loading page.
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
def driver(wait_for_site):
    """
    Create a new Firefox browser for each test and close it afterward.
    """
    browser = webdriver.Firefox()
    browser.set_page_load_timeout(120)

    yield browser

    browser.quit()