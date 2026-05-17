# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase


class TC_003_001_DataDriven(MoodleDataDrivenTestCase):
    TEST_CASE = "TC-003-001"
    DATA_FILE = "tc_003_001_data.csv"

    def test_tc_003_001_data_driven(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                self.log_step("Open Moodle home")
                self.driver.get(row["site_url"])
                self.login(row)
                self.log_step("Open course using stable course locator")
                self.click(By.XPATH, row["course_xpath"])
                self.log_step("Verify insert button is hidden before edit mode")
                self.assertFalse(self.is_element_present(By.XPATH, row["insert_button_xpath"]))
                self.log_step("Enable edit mode")
                self.click(By.XPATH, row["edit_mode_checkbox_xpath"])
                self.log_step("Verify insert button is visible after edit mode")
                self.wait_for_stable_element(By.XPATH, row["insert_button_xpath"], timeout=30)



if __name__ == "__main__":
    unittest.main()
