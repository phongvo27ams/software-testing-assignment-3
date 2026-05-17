# -*- coding: utf-8 -*-
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


SITE_URL = "https://school.moodledemo.net/"
LOGIN_URL = "https://school.moodledemo.net/login/index.php"
PARTICIPANTS_URL = "https://school.moodledemo.net/user/index.php?id=69"
TEACHER_USERNAME = "teacher"
TEACHER_PASSWORD = "moodle26"
EXPLICIT_WAIT = 30
AUTOCOMPLETE_WAIT = 3


def teacher_login_row():
    return {
        "site_url": SITE_URL,
        "login_url": LOGIN_URL,
        "username": TEACHER_USERNAME,
        "password": TEACHER_PASSWORD,
    }


def login_as_teacher(test_case):
    test_case.login(teacher_login_row())


def js_click(test_case, element):
    test_case.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    test_case.driver.execute_script("arguments[0].click();", element)


def is_element_present(driver, by, value):
    try:
        driver.find_element(by=by, value=value)
    except NoSuchElementException:
        return False
    return True


def unenrol_if_enrolled(test_case, user_name):
    if not user_name:
        return

    driver = test_case.driver
    driver.get(PARTICIPANTS_URL)
    time.sleep(1.5)

    trash_xpath = (
        "//tr[contains(.,%r)]"
        "//a[.//*[contains(@class,'fa-trash')] "
        "or contains(@title,'Delete enrolment') "
        "or contains(@title,'Unenrol') "
        "or contains(@data-action,'unenrol')]"
    ) % user_name

    trash_icons = driver.find_elements(By.XPATH, trash_xpath)
    if not trash_icons:
        return

    js_click(test_case, trash_icons[0])
    time.sleep(1)

    try:
        confirm_button = WebDriverWait(driver, 8).until(
            lambda d: d.find_element(
                By.XPATH,
                "//button[contains(.,'Unenrol') or contains(.,'unenrol') "
                "or contains(.,'Yes') or contains(.,'Confirm') "
                "or contains(.,'Delete enrolment')]",
            )
        )
        js_click(test_case, confirm_button)
        time.sleep(1)
    except TimeoutException:
        pass


def open_enrol_dialog(test_case):
    driver = test_case.driver
    driver.get(PARTICIPANTS_URL)
    enrol_button = WebDriverWait(driver, EXPLICIT_WAIT).until(
        lambda d: d.find_element(By.XPATH, "//input[@value='Enrol users']")
    )
    js_click(test_case, enrol_button)


def type_in_user_search(test_case, text):
    search_box = WebDriverWait(test_case.driver, EXPLICIT_WAIT).until(
        lambda d: d.find_element(
            By.XPATH,
            "//div[contains(@class,'form-autocomplete-input')]/input[@placeholder='Search']",
        )
    )
    search_box.click()
    search_box.clear()
    if text:
        search_box.send_keys(text)
    time.sleep(AUTOCOMPLETE_WAIT)


def select_user_suggestion(test_case, user_name):
    suggestion = WebDriverWait(test_case.driver, EXPLICIT_WAIT).until(
        lambda d: d.find_element(By.XPATH, "//li[contains(.,%r)]" % user_name)
    )
    js_click(test_case, suggestion)


def search_and_select_user(test_case, keyword, user_name):
    type_in_user_search(test_case, keyword)
    select_user_suggestion(test_case, user_name)


def select_role(test_case, role):
    Select(test_case.driver.find_element(By.ID, "id_roletoassign")).select_by_visible_text(role)


def expand_show_more(test_case):
    show_more = test_case.driver.find_element(By.XPATH, "//a[contains(.,'Show more')]")
    js_click(test_case, show_more)
    time.sleep(0.5)


def select_value_if_present(driver, element_id, value):
    elements = driver.find_elements(By.ID, element_id)
    if elements:
        Select(elements[0]).select_by_value(value)


def set_enrol_dates(test_case, row):
    driver = test_case.driver
    expand_show_more(test_case)

    Select(driver.find_element(By.ID, "id_startdate")).select_by_value("5")
    time.sleep(0.5)
    Select(driver.find_element(By.ID, "id_startdateselect_day")).select_by_visible_text(row["start_day"])
    Select(driver.find_element(By.ID, "id_startdateselect_month")).select_by_visible_text(row["start_month"])
    Select(driver.find_element(By.ID, "id_startdateselect_year")).select_by_visible_text(row["start_year"])
    select_value_if_present(driver, "id_startdateselect_hour", "0")
    select_value_if_present(driver, "id_startdateselect_minute", "0")

    if row["end_enabled"].strip().lower() == "true":
        driver.find_element(By.ID, "id_timeend_enabled").click()
        time.sleep(0.5)
        Select(driver.find_element(By.ID, "id_timeend_day")).select_by_visible_text(row["end_day"])
        Select(driver.find_element(By.ID, "id_timeend_month")).select_by_visible_text(row["end_month"])
        Select(driver.find_element(By.ID, "id_timeend_year")).select_by_visible_text(row["end_year"])
        select_value_if_present(driver, "id_timeend_hour", "23")
        select_value_if_present(driver, "id_timeend_minute", "55")


def click_enrol_selected(test_case):
    button = test_case.driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Enrol selected users and cohorts')]",
    )
    js_click(test_case, button)
    time.sleep(1)


def validation_error_present(driver):
    return bool(visible_error_texts(driver))


def visible_error_texts(driver):
    error_xpath = (
        "//div[contains(@class,'alert-danger')] | "
        "//div[contains(@class,'invalid-feedback')] | "
        "//div[contains(@class,'form-control-feedback')] | "
        "//span[contains(@class,'error') and normalize-space(.)!='']"
    )
    texts = []
    for element in driver.find_elements(By.XPATH, error_xpath):
        if element.is_displayed() and element.text.strip():
            texts.append(element.text.strip())
    return texts


def user_visible_on_participants_page(test_case, user_name):
    if not user_name:
        return False
    test_case.driver.get(PARTICIPANTS_URL)
    time.sleep(1)
    return is_element_present(test_case.driver, By.XPATH, "//tr[contains(.,%r)]" % user_name)


def assert_pass_fail_result(test_case, expected_result, user_name=None):
    expected = (expected_result or "").strip().lower()
    errors = visible_error_texts(test_case.driver)
    error_present = bool(errors)
    if expected == "pass":
        test_case.assertFalse(
            error_present,
            "Expected successful enrolment but an error appeared: %s" % " | ".join(errors),
        )
        if user_name:
            test_case.assertTrue(
                user_visible_on_participants_page(test_case, user_name),
                "Expected enrolled user to be visible on Participants page.",
            )
    elif expected == "fail":
        test_case.assertTrue(error_present, "Expected validation error but none appeared.")
    else:
        raise AssertionError("Unsupported expected_result: %s" % expected_result)


def suggestion_visible(driver, user_name):
    if not user_name:
        return False
    return is_element_present(driver, By.XPATH, "//li[contains(.,%r)]" % user_name)


def any_suggestion_visible(driver):
    return is_element_present(
        driver,
        By.XPATH,
        "//ul[contains(@class,'form-autocomplete-suggestions')]/li[not(contains(@class,'loading'))]",
    )
