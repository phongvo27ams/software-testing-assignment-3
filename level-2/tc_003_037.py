# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase


class TC_003_037_DataDriven(MoodleDataDrivenTestCase):
    TEST_CASE = "TC-003-037"
    DATA_FILE = "tc_003_030_data.csv"

    def test_tc_003_037_data_driven(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                moodle_quiz_prepare.prepare_multiple_choice_question_form(self, row)
                self.log_step("Enter question name")
                self.type_text(By.ID, row["question_name_input_id"], row["question_name"])
                self.log_step("Enter question text")
                self.set_editor_text_by_data_id(row["question_text_data_id"], row["question_text"])
                self.log_step("Enter default mark")
                self.type_text(By.ID, row["defaultmark_input_id"], row["defaultmark_value"])
                self.log_step("Enter answer 1")
                self.set_editor_text_by_data_id(row["answer_0_data_id"], row["answer_0_text"])
                self.log_step("Select answer 1 grade")
                self.select_option_by_visible_text(row["fraction_0_select_id"], row["fraction_0_option_text"])
                if row["answer_1_text"]:
                    self.log_step("Enter answer 2")
                    self.set_editor_text_by_data_id(row["answer_1_data_id"], row["answer_1_text"])
                if row["fraction_1_option_text"]:
                    self.log_step("Select answer 2 grade")
                    self.select_option_by_visible_text(row["fraction_1_select_id"], row["fraction_1_option_text"])
                self.log_step("Save question")
                self.click(By.ID, row["submit_button_id"])
                self.log_step("Verify expected result")
                self.assert_expected_result(row)



if __name__ == "__main__":
    unittest.main()
