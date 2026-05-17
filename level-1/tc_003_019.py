# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase


class TC_003_019_DataDriven(MoodleDataDrivenTestCase):
    TEST_CASE = "TC-003-019"
    DATA_FILE = "tc_003_014_data.csv"

    def test_tc_003_019_data_driven(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                moodle_quiz_prepare.prepare_new_quiz_form(self, row, verify_heading=False)
                self.log_step("Enter quiz name")
                self.type_text(By.ID, row["name_input_id"], row["quiz_name"])
                self.log_step("Open Grade section")
                self.click(By.XPATH, row["grade_toggle_xpath"])
                self.log_step("Enter grade to pass")
                self.type_text(By.ID, row["gradepass_id"], row["gradepass_value"])
                self.log_step("Save and display")
                self.click(By.XPATH, row["save_button_xpath"])
                self.log_step("Verify expected result")
                if row["expected_type"] == "text":
                    expected_xpath = "//p[normalize-space(.) = %r]" % row["expected_grade_text"]
                    self.assertEqual(row["expected_grade_text"], self.wait_for_stable_element(By.XPATH, expected_xpath).text)
                elif row["expected_type"] == "body_not_contains":
                    self.assertNotIn(row["expected_grade_text"], self.driver.find_element_by_css_selector("BODY").text)
                elif row["expected_type"] == "error_id":
                    error = self.wait_for_stable_element(By.ID, row["expected_error_id"])
                    self.assertEqual(row["expected_error_text"], error.text)
                else:
                    error = self.wait_for_stable_element(By.XPATH, row["expected_error_xpath"])
                    self.assertIn(row["expected_error_text"], error.text)



if __name__ == "__main__":
    unittest.main()
