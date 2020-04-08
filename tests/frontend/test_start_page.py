import pytest
from selenium.webdriver import Firefox, FirefoxOptions


@pytest.fixture
def browser():
    options = FirefoxOptions()
    options.headless = True
    driver = Firefox(
        executable_path="/Users/amir/makmal/geckodriver/geckodriver",
        # options=options,
    )
    yield driver
    driver.close()


def test_start_page(browser):

    browser.get("http://localhost:8000")

    name_field = browser.find_element_by_id("nameField")
    table_key_field = browser.find_element_by_id("tableKeyfield")
    join_create_table_button = browser.find_element_by_id("joinCreateTable")

    assert name_field
    assert table_key_field
    assert join_create_table_button


def test_can_create_table(browser):

    browser.get("http://localhost:8000")

    name_field = browser.find_element_by_id("nameField")
    name_field.send_keys("player")
    join_create_table_button = browser.find_element_by_id("joinCreateTable")
    join_create_table_button.click()
    table_cards_div = browser.find_element_by_id("tableCards")
    assert "Table" in table_cards_div.text
    table_cards = browser.find_elements_by_class_name("card")
    assert len(table_cards) == 13 * 4


def test_can_join_table(browser):

    browser.get("http://localhost:8000")

    name_field = browser.find_element_by_id("nameField")
    name_field.send_keys("player")
    join_create_table_button = browser.find_element_by_id("joinCreateTable")
    join_create_table_button.click()

    browser.get("http://localhost:8000")

    name_field = browser.find_element_by_id("nameField")
    name_field.send_keys("player2")
    join_create_table_button = browser.find_element_by_id("joinCreateTable")
    join_create_table_button.click()
