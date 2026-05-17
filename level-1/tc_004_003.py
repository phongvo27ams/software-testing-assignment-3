# -*- coding: utf-8 -*-
import time
import unittest

from selenium.webdriver.common.by import By

import moodle_enrol_helpers as enrol
from moodle_test_base import MoodleDataDrivenTestCase


class TC_004_003_EnrolSearch(MoodleDataDrivenTestCase):
    DATA_FILE = "tc_004_003_data.csv"
    LOG_PREFIX = "TC-004-003"

    def test_enrol_search_variations(self):
        for index, row in enumerate(self.rows()):
            if index > 0:
                self.restart_driver()
            with self.subTest(row["tc_id"]):
                self.log_step("Login as teacher")
                enrol.login_as_teacher(self)
                self.log_step("Clean existing enrolment")
                enrol.unenrol_if_enrolled(self, row["user_name"])
                self.log_step("Open enrol users dialog")
                enrol.open_enrol_dialog(self)
                self.log_step("Type search input")
                enrol.type_in_user_search(self, row["search_input"])
                self.verify_search_result(row)

    def verify_search_result(self, row):
        user_name = row["user_name"].strip()
        expected_found = row["user_found"].strip().lower() == "true"
        should_enrol = row["should_enrol"].strip().lower() == "true"

        actual_found = enrol.suggestion_visible(self.driver, user_name) if user_name else enrol.any_suggestion_visible(self.driver)
        self.assertEqual(expected_found, actual_found)

        if should_enrol and user_name:
            if row["tc_id"] == "TC004013":
                self.driver.find_element(By.XPATH, "//li[contains(.,%r)]" % user_name).click()
                time.sleep(1)
                self.assertFalse(enrol.suggestion_visible(self.driver, user_name))
                enrol.click_enrol_selected(self)
            else:
                enrol.select_user_suggestion(self, user_name)
                enrol.click_enrol_selected(self)
            enrol.assert_pass_fail_result(self, row["expected_result"], user_name)


if __name__ == "__main__":
    unittest.main()
