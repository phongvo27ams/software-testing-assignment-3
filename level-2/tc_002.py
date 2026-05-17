# -*- coding: utf-8 -*-
import random
import unittest

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from moodle_test_base import MoodleDataDrivenTestCase


class TC_002_CourseCreationDataDrivenLevel2(MoodleDataDrivenTestCase):
    DATA_FILE = "tc_002_data.csv"
    LOG_PREFIX = "L2-TC-002"

    SITE_URL = "https://school.moodledemo.net/"
    LOGIN_URL = "https://school.moodledemo.net/login/index.php"
    MANAGER_USERNAME = "manager"
    MANAGER_PASSWORD = "moodle26"

    def setUp(self):
        super(TC_002_CourseCreationDataDrivenLevel2, self).setUp()
        self.session_suffix = "_%s" % random.randint(1000, 9999)

    def test_course_creation_data_driven(self):
        for index, row in enumerate(self.read_data()):
            if index > 0:
                self.restart_driver()
                self.session_suffix = "_%s" % random.randint(1000, 9999)
            with self.subTest(row["test_id"]):
                self.log_step("Login as manager")
                self.login_as_manager()
                self.log_step("Open course creation form")
                self.open_course_creation_form(row)
                self.log_step("Fill course form")
                created_fullname = self.fill_course_form(row)
                self.log_step("Save and verify")
                self.save_and_verify(row, created_fullname)

    def login_as_manager(self):
        self.login(
            {
                "site_url": self.SITE_URL,
                "login_url": self.LOGIN_URL,
                "username": self.MANAGER_USERNAME,
                "password": self.MANAGER_PASSWORD,
            }
        )

    def open_course_creation_form(self, row):
        self.driver.get(row["course_url"])
        self.wait_for_stable_element(By.ID, row["fullname_loc"])

    def fill_course_form(self, row):
        fullname = self.unique_value(row["fullname"])
        shortname = self.unique_value(row["shortname"])

        self.type_text(By.ID, row["fullname_loc"], fullname)
        self.type_text(By.ID, row["shortname_loc"], shortname)
        self.select_category(row)

        if row["numsections"].strip():
            self.expand_section(row["course_format_sec"])
            self.select_visible_text(row["numsections_loc"], row["numsections"])

        if row["newsitems"].strip():
            self.expand_section(row["appearances_sec"])
            self.select_visible_text(row["newsitems_loc"], row["newsitems"])

        if row["credits"].strip():
            self.expand_section(row["custom_fields_sec"])
            self.type_text(By.ID, row["credits_loc"], row["credits"])

        self.set_course_dates(row)
        return fullname

    def unique_value(self, value):
        value = (value or "").strip()
        return "%s%s" % (value, self.session_suffix) if value else ""

    def select_category(self, row):
        category = (row["category"] or "").strip()
        if not category:
            self.clear_current_category(row)
            return

        current_text = ""
        try:
            current_text = self.driver.find_element(By.CSS_SELECTOR, row["category_clear_loc"]).text
        except Exception:
            pass

        if category in current_text:
            return

        self.clear_current_category(row)
        self.click(By.CSS_SELECTOR, row["category_arrow_loc"])
        suggestion_xpath = (
            "//ul[contains(@id, 'form_autocomplete_suggestions')]"
            "/li[normalize-space(.)=%r]"
        ) % category
        for attempt in range(3):
            try:
                self.click(By.XPATH, suggestion_xpath)
                return
            except StaleElementReferenceException:
                if attempt == 2:
                    raise

    def clear_current_category(self, row):
        try:
            self.click(By.CSS_SELECTOR, row["category_clear_loc"], timeout=2)
        except Exception:
            pass

    def expand_section(self, collapse_id):
        try:
            section = self.wait_for_stable_element(By.ID, collapse_id, timeout=5)
            if section.get_attribute("aria-expanded") != "true":
                self.driver.execute_script("arguments[0].click();", section)
        except Exception:
            pass

    def select_visible_text(self, select_id, visible_text):
        select = self.wait_for_stable_element(By.ID, select_id)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select)
        try:
            Select(select).select_by_visible_text(visible_text)
        except Exception:
            self.select_option_by_visible_text(select_id, visible_text)

    def set_course_dates(self, row):
        if row["start_day"].strip():
            self.select_visible_text("id_startdate_day", row["start_day"])
            self.select_visible_text("id_startdate_month", row["start_month"])
            self.select_visible_text("id_startdate_year", row["start_year"])
            self.select_visible_text("id_startdate_hour", row["start_hour"])
            self.select_visible_text("id_startdate_minute", self.two_digit_minute(row["start_minute"]))

        if row["end_day"].strip():
            if row["use_automatic_enddate"].strip().upper() != "TRUE":
                self.disable_automatic_enddate(row)
            self.select_visible_text("id_enddate_day", row["end_day"])
            self.select_visible_text("id_enddate_month", row["end_month"])
            self.select_visible_text("id_enddate_year", row["end_year"])
            self.select_visible_text("id_enddate_hour", row["end_hour"])
            self.select_visible_text("id_enddate_minute", self.two_digit_minute(row["end_minute"]))

    def disable_automatic_enddate(self, row):
        try:
            checkbox = self.wait_for_stable_element(By.ID, row["auto_enddate_loc"], timeout=5)
            if checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)
        except TimeoutException:
            pass

    def two_digit_minute(self, value):
        value = (value or "").strip()
        return "%02d" % int(value) if value.isdigit() else value

    def save_and_verify(self, row, created_fullname):
        save_button = self.wait_for_stable_element(By.ID, row["save_btn_loc"])
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)

        verification_type = row["verification_type"].strip()
        if verification_type == "error_element":
            self.verify_form_error(row, save_button)
        else:
            self.verify_course_created(row, created_fullname, save_button, verification_type)

    def verify_form_error(self, row, save_button):
        self.driver.execute_script("arguments[0].click();", save_button)
        error = self.wait_for_stable_element(By.ID, row["error_element_id"])
        actual_text = self.normalize_text(error.text).replace(self.session_suffix, "")
        self.assertIn(self.normalize_text(row["expected_text"]), actual_text)

    def verify_course_created(self, row, created_fullname, save_button, xpath_to_verify):
        self.driver.execute_script("arguments[0].click();", save_button)
        WebDriverWait(self.driver, 30).until(lambda driver: "edit.php" not in driver.current_url)

        self.driver.get(row["manage_url"])
        self.wait_for_stable_element(By.ID, "action_bar")

        search_input = self.wait_for_stable_element(By.XPATH, "//div[2]/div/form/div/input")
        search_input.clear()
        search_input.send_keys(created_fullname)
        search_input.send_keys(Keys.ENTER)
        try:
            WebDriverWait(self.driver, 5).until(lambda driver: search_input.id not in driver.page_source)
        except Exception:
            pass

        resolved_xpath = xpath_to_verify or "//div[contains(@class, 'course-amount')]"
        if "yui_3_18" in resolved_xpath:
            resolved_xpath = (
                "%s | //div[contains(@class, 'course-amount')] | "
                "//div[starts-with(@id, 'yui_3_18_1_1_')]/div"
            ) % resolved_xpath

        result = self.wait_for_stable_element(By.XPATH, resolved_xpath)
        self.assertEqual(
            self.normalize_text(row["expected_text"]),
            self.normalize_text(result.text),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
