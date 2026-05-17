# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase


class TC_003_024_DataDriven(MoodleDataDrivenTestCase):
    TEST_CASE = "TC-003-024"
    DATA_FILE = "tc_003_021_data.csv"

    def test_tc_003_024_data_driven(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                moodle_quiz_prepare.prepare_new_quiz_form(self, row, verify_heading=False)
                self.log_step("Enter quiz name")
                self.type_text(By.ID, row["name_input_id"], row["quiz_name"])
                if row["quizpassword_value"]:
                    self.log_step("Open Security section")
                    self.click(By.XPATH, row["security_toggle_xpath"])
                    self.log_step("Click password display value toggle")
                    self.click(By.XPATH, row["password_unmask_xpath"])
                    self.log_step("Enter quiz password")
                    self.type_text_or_set_value(By.ID, row["quizpassword_id"], row["quizpassword_value"])
                self.log_step("Save and display")
                self.click(By.XPATH, row["save_button_xpath"])
                self.log_step("Verify expected result")
                self.assert_expected_result(row)



if __name__ == "__main__":
    unittest.main()
