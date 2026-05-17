# -*- coding: utf-8 -*-
import csv
import time
import unittest
from pathlib import Path

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from moodle_test_base import MoodleDataDrivenTestCase


BY_MAP = {
    "id": By.ID,
    "xpath": By.XPATH,
    "name": By.NAME,
    "css": By.CSS_SELECTOR,
    "class": By.CLASS_NAME,
    "tag": By.TAG_NAME,
}


class TC_004_EnrolDataDrivenLevel2(MoodleDataDrivenTestCase):
    DATA_FILE = "tc_004_data.csv"
    LOG_PREFIX = "L2-TC-004"
    CONFIG_FILE = "tc_004_config.csv"
    LOCATORS_FILE = "tc_004_locators.csv"

    def setUp(self):
        super(TC_004_EnrolDataDrivenLevel2, self).setUp()
        self.config = self.load_config()
        self.locators = self.load_locators()

    def load_config(self):
        path = Path(__file__).resolve().parent / "data" / self.CONFIG_FILE
        with open(path, newline="", encoding="utf-8-sig") as csv_file:
            return {row["key"].strip(): row["value"].strip() for row in csv.DictReader(csv_file)}

    def load_locators(self):
        path = Path(__file__).resolve().parent / "data" / self.LOCATORS_FILE
        locators = {}
        with open(path, newline="", encoding="utf-8-sig") as csv_file:
            for row in csv.DictReader(csv_file):
                locators[row["element_name"].strip()] = (
                    BY_MAP[row["by"].strip().lower()],
                    row["value"].strip(),
                )
        return locators

    def read_data(self):
        path = Path(__file__).resolve().parent / "data" / self.DATA_FILE
        with open(path, newline="", encoding="utf-8-sig") as csv_file:
            return list(csv.DictReader(csv_file))

    def test_enrol_users_data_driven(self):
        for index, row in enumerate(self.read_data()):
            if index > 0:
                self.restart_driver()
                self.config = self.load_config()
                self.locators = self.load_locators()
            with self.subTest(row["tc_id"]):
                self.log_step("Login as teacher")
                self.login_from_config()
                self.log_step("Clean existing enrolment")
                self.unenrol_if_enrolled(row["user_name"])
                self.log_step("Open enrol users dialog")
                self.open_enrol_dialog()
                self.log_step("Search user")
                self.search_user(row["search_keyword"])
                self.log_step("Select role")
                self.select_role(row["role"])
                self.log_step("Select user")
                self.select_user(row["user_name"])
                self.log_step("Set enrolment dates")
                self.set_enrol_dates(row)
                self.log_step("Enrol selected user")
                self.click_enrol_selected()
                self.log_step("Verify expected result")
                self.assert_pass_fail_result(row)

    def locator(self, name):
        return self.locators[name]

    def wait_locator(self, name, timeout=30):
        by, value = self.locator(name)
        return self.wait_for_stable_element(by, value, timeout=timeout)

    def click_locator(self, name, timeout=30):
        by, value = self.locator(name)
        return self.click(by, value, timeout=timeout)

    def login_from_config(self):
        self.driver.get(self.config["login_url"])
        self.type_text(*self.locator("username_field"), value=self.config["username"])
        self.type_text(*self.locator("password_field"), value=self.config["password"])
        self.click_locator("login_button")
        WebDriverWait(self.driver, 20).until(lambda driver: self.is_logged_in())

    def unenrol_if_enrolled(self, user_name):
        if not user_name:
            return
        self.driver.get(self.config["participants_url"])
        time.sleep(1)

        row_xpath = self.template("participant_user_row_xpath", user_name=user_name)
        trash_xpath = self.template("unenrol_button_in_user_row_xpath", user_name=user_name)
        if not self.elements_present(By.XPATH, row_xpath):
            return

        trash_buttons = self.driver.find_elements(By.XPATH, trash_xpath)
        if not trash_buttons:
            return

        self.js_click(trash_buttons[0])
        try:
            confirm = self.wait_for_stable_element(*self.locator("unenrol_confirm_button"), timeout=8)
            self.js_click(confirm)
            time.sleep(1)
        except TimeoutException:
            pass

    def open_enrol_dialog(self):
        self.driver.get(self.config["participants_url"])
        self.click_locator("enrol_users_button")

    def search_user(self, keyword):
        search_box = self.wait_locator("search_box")
        search_box.click()
        search_box.clear()
        if keyword:
            search_box.send_keys(keyword)
        time.sleep(float(self.config.get("autocomplete_wait_seconds", "3")))

    def select_role(self, role):
        if role and role.strip():
            Select(self.wait_locator("role_select")).select_by_visible_text(role.strip())

    def select_user(self, user_name):
        user_xpath = self.template("user_suggestion_xpath", user_name=user_name)
        self.click(By.XPATH, user_xpath)

    def set_enrol_dates(self, row):
        if not row["start_day"].strip():
            return

        try:
            self.click_locator("show_more_link", timeout=5)
        except Exception:
            pass

        Select(self.wait_locator("start_date_select")).select_by_value("5")
        Select(self.wait_locator("start_day_select")).select_by_visible_text(row["start_day"])
        Select(self.wait_locator("start_month_select")).select_by_visible_text(row["start_month"])
        Select(self.wait_locator("start_year_select")).select_by_visible_text(row["start_year"])
        self.select_value_if_locator_exists("start_hour_select", "0")
        self.select_value_if_locator_exists("start_minute_select", "0")

        if row["end_enabled"].strip().lower() == "true":
            checkbox = self.wait_locator("end_enabled_checkbox")
            if not checkbox.is_selected():
                self.js_click(checkbox)
            Select(self.wait_locator("end_day_select")).select_by_visible_text(row["end_day"])
            Select(self.wait_locator("end_month_select")).select_by_visible_text(row["end_month"])
            Select(self.wait_locator("end_year_select")).select_by_visible_text(row["end_year"])
            self.select_value_if_locator_exists("end_hour_select", "23")
            self.select_value_if_locator_exists("end_minute_select", "55")

    def select_value_if_locator_exists(self, locator_name, value):
        if locator_name not in self.locators:
            return
        elements = self.driver.find_elements(*self.locator(locator_name))
        if elements:
            Select(elements[0]).select_by_value(value)

    def click_enrol_selected(self):
        self.click_locator("submit_enrol_button")
        time.sleep(1)

    def assert_pass_fail_result(self, row):
        expected = row["expected_result"].strip().lower()
        errors = self.visible_error_texts()
        if expected == "pass":
            self.assertFalse(
                errors,
                "Expected successful enrolment but an error appeared: %s" % " | ".join(errors),
            )
            self.assertTrue(
                self.user_visible_on_participants_page(row["user_name"]),
                "Expected enrolled user to be visible on Participants page.",
            )
        elif expected == "fail":
            self.assertTrue(errors, "Expected validation error but none appeared.")
        else:
            raise AssertionError("Unsupported expected_result: %s" % row["expected_result"])

    def visible_error_texts(self):
        texts = []
        for name in ("error_message_danger", "error_message_feedback", "error_message_span"):
            if name not in self.locators:
                continue
            for element in self.driver.find_elements(*self.locator(name)):
                if element.is_displayed() and element.text.strip():
                    texts.append(element.text.strip())
        return texts

    def user_visible_on_participants_page(self, user_name):
        self.driver.get(self.config["participants_url"])
        time.sleep(1)
        return self.elements_present(By.XPATH, self.template("participant_user_row_xpath", user_name=user_name))

    def elements_present(self, by, value):
        try:
            self.driver.find_element(by=by, value=value)
        except NoSuchElementException:
            return False
        return True

    def js_click(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    def template(self, locator_name, **values):
        return self.locators[locator_name][1].format(**values)


if __name__ == "__main__":
    unittest.main(verbosity=2)
