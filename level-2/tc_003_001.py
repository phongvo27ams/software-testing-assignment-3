# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By

from moodle_test_base import MoodleDataDrivenTestCase


class TC_003_001_Level2(MoodleDataDrivenTestCase):
    TEST_CASE = "TC-003-001"
    DATA_FILE = "tc_003_001_level2_data.csv"

    def login(self, row):
        level1_row = dict(row)
        level1_row["login_url"] = row["login_page_url"]
        super().login(level1_row)

    def test_tc_003_001_level2_data_driven_items(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                self.log_step("Open Moodle home page from data file")
                self.driver.get(row["home_url"])

                self.login(row)

                self.log_step("Open course using course locator from data file")
                self.click(By.XPATH, row["course_link_xpath"])

                self.log_step("Verify insert content button state before edit mode")
                if row["expected_before_edit_mode"] == "hidden":
                    self.assertFalse(self.is_element_present(By.XPATH, row["insert_content_button_xpath"]))
                else:
                    self.wait_for_stable_element(By.XPATH, row["insert_content_button_xpath"])

                self.log_step("Enable edit mode using toggle locator from data file")
                self.click(By.XPATH, row["edit_mode_toggle_xpath"])

                self.log_step("Verify insert content button state after edit mode")
                if row["expected_after_edit_mode"] == "visible":
                    self.wait_for_stable_element(By.XPATH, row["insert_content_button_xpath"], timeout=30)
                else:
                    self.assertFalse(self.is_element_present(By.XPATH, row["insert_content_button_xpath"]))


if __name__ == "__main__":
    unittest.main()
