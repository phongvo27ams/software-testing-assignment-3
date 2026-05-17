# -*- coding: utf-8 -*-
import csv
import sys
import time
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
LEVEL_1_DIR = ROOT_DIR / "level-1"
sys.path.insert(0, str(LEVEL_1_DIR))

from moodle_test_base import MoodleDataDrivenTestCase
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By


class EnrolmentSearchSecurityTest(MoodleDataDrivenTestCase):
    TEST_CASE = "NF-TC-004-002"
    DATA_FILE = "nf_tc_004_002_data.csv"
    LOG_PREFIX = "NF-TC-004-002"

    def read_data(self):
        data_file = Path(__file__).resolve().parent / "data" / self.DATA_FILE
        with open(data_file, newline="", encoding="utf-8-sig") as csv_file:
            return list(csv.DictReader(csv_file))

    def test_search_input_injection_payloads(self):
        for index, row in enumerate(self.read_data()):
            if index > 0:
                self.restart_driver()
            with self.subTest(row["payload_id"]):
                self.log_step("Login as teacher")
                self.login(row)
                self.log_step("Open enrol dialog")
                self.open_enrol_dialog(row)
                self.log_step("Submit payload")
                self.submit_payload(row)
                self.log_step("Verify security expectations")
                self.assert_no_alert(row)
                self.assert_page_stable(row)
                self.assert_no_sensitive_leak(row)
                self.assert_no_raw_script_reflection(row)

    def open_enrol_dialog(self, row):
        self.driver.get(row["participants_url"])
        self.click(By.XPATH, row["enrol_users_button_xpath"])
        self.wait_for_stable_element(By.XPATH, row["search_box_xpath"])

    def submit_payload(self, row):
        search_box = self.wait_for_stable_element(By.XPATH, row["search_box_xpath"])
        search_box.click()
        search_box.clear()
        try:
            search_box.send_keys(row["payload"])
        except UnexpectedAlertPresentException:
            self.fail("XSS alert triggered while entering payload: %s" % self.dismiss_alert_if_present())
        time.sleep(float(row["wait_after_input_seconds"]))

    def assert_no_alert(self, row):
        alert_text = self.dismiss_alert_if_present()
        self.assertIsNone(alert_text, "[%s] Unexpected alert: %s" % (row["payload_id"], alert_text))

    def assert_page_stable(self, row):
        self.assertIn(row["expected_domain"], self.driver.current_url)

    def assert_no_sensitive_leak(self, row):
        page_source = self.driver.page_source.lower()
        for keyword in self.split_pipe_values(row["forbidden_keywords"]):
            self.assertNotIn(keyword.lower(), page_source)

    def assert_no_raw_script_reflection(self, row):
        if "<script>" not in row["payload"].lower():
            return
        self.assertNotIn("<script>alert", self.driver.page_source.lower())

    def dismiss_alert_if_present(self):
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.dismiss()
            return text
        except NoAlertPresentException:
            return None

    def split_pipe_values(self, value):
        return [item.strip() for item in (value or "").split("|") if item.strip()]


if __name__ == "__main__":
    unittest.main(verbosity=2)
