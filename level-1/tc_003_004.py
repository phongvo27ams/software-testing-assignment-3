# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase


class TC_003_004_DataDriven(MoodleDataDrivenTestCase):
    TEST_CASE = "TC-003-004"
    DATA_FILE = "tc_003_004_data.csv"

    def test_tc_003_004_data_driven(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                moodle_quiz_prepare.prepare_new_quiz_form(self, row, verify_heading=False)
                self.log_step("Enter quiz name")
                self.type_text(By.ID, row["name_input_id"], row["quiz_name"])
                self.log_step("Enter quiz description")
                self.type_rich_text_html(row["description_editor_aria_label"], row["description_html"])
                self.log_step("Open Timing section")
                self.click(By.XPATH, row["timing_toggle_xpath"])
                self.log_step("Enable time limit")
                self.ensure_checkbox_checked(row["time_limit_enabled_id"])
                self.log_step("Open Grade section")
                self.click(By.XPATH, row["grade_toggle_xpath"])
                self.log_step("Enter time limit")
                self.type_text(By.ID, row["time_limit_number_id"], row["time_limit_value"])
                self.log_step("Enter grade to pass")
                self.type_text(By.ID, row["gradepass_id"], row["gradepass_value"])
                self.log_step("Open Security section")
                self.click(By.XPATH, row["security_toggle_xpath"])
                self.log_step("Click password display value toggle")
                self.click(By.XPATH, row["password_unmask_xpath"])
                self.log_step("Enter quiz password")
                self.type_text_or_set_value(By.ID, row["quizpassword_id"], row["quizpassword_value"])
                self.log_step("Save and display")
                self.click(By.XPATH, row["save_button_xpath"])
                self.log_step("Verify password requirement")
                self.assertEqual(row["expected_password_text"], self.wait_for_stable_element(By.XPATH, row["expected_password_xpath"]).text)
                self.log_step("Verify time limit")
                self.assertEqual(row["expected_time_limit_text"], self.wait_for_stable_element(By.XPATH, row["expected_time_limit_xpath"]).text)
                self.log_step("Verify grade to pass")
                self.assertEqual(row["expected_grade_text"], self.wait_for_stable_element(By.XPATH, row["expected_grade_xpath"]).text)



if __name__ == "__main__":
    unittest.main()
