# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase


class TC_003_028_029_DataDriven(MoodleDataDrivenTestCase):
    DATA_FILE = "tc_003_028_data.csv"

    def test_data_driven_group(self):
        for index, row in enumerate(self.rows()):
            if index > 0:
                self.restart_driver()
            with self.subTest(row["test_case"]):
                moodle_quiz_prepare.prepare_multiple_choice_question_form(self, row)
                self.log_step("Enter question name")
                self.type_text(By.ID, row["question_name_input_id"], row["question_name"])
                self.log_step("Enter question text")
                self.set_editor_text_by_data_id(row["question_text_data_id"], row["question_text"])
                self.log_step("Enter answer 1")
                self.set_editor_text_by_data_id(row["answer_0_data_id"], row["answer_0_text"])
                self.log_step("Select answer 1 grade")
                self.select_option_by_visible_text(row["fraction_0_select_id"], row["fraction_0_option_text"])
                self.log_step("Enter answer 2")
                self.set_editor_text_by_data_id(row["answer_1_data_id"], row["answer_1_text"])
                self.log_step("Save question")
                self.click(By.ID, row["submit_button_id"])
                self.log_step("Verify expected error")
                error = self.wait_for_stable_element(By.ID, row["expected_error_id"])
                self.assertEqual(row["expected_error_text"], error.text)



if __name__ == "__main__":
    unittest.main()
