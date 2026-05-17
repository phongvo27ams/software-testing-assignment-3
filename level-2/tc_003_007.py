# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase


class TC_003_007_DataDriven(MoodleDataDrivenTestCase):
    TEST_CASE = "TC-003-007"
    DATA_FILE = "tc_003_007_data.csv"

    def test_tc_003_007_data_driven(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                moodle_quiz_prepare.prepare_new_quiz_form(self, row, verify_heading=False)
                self.log_step("Enter quiz name")
                self.type_text(By.ID, row["name_input_id"], row["quiz_name"])
                self.log_step("Save and display")
                self.click(By.XPATH, row["save_button_xpath"])
                self.log_step("Verify expected result")
                if row["expected_error_id"]:
                    error = self.wait_for_stable_element(By.ID, row["expected_error_id"])
                    self.assertEqual(row["expected_error_text"], error.text)
                else:
                    heading = self.wait_for_stable_element(By.XPATH, row["expected_heading_xpath"])
                    self.assertEqual(row["quiz_name"], heading.text)



if __name__ == "__main__":
    unittest.main()
