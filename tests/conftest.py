import pytest
from selenium import webdriver


@pytest.fixture
def base_url():
    return "http://127.0.0.1:5000"


@pytest.fixture
def driver():
    browser = webdriver.Firefox()

    yield browser

    browser.quit()