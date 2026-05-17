# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase


class TC_003_025_DataDriven(MoodleDataDrivenTestCase):
    TEST_CASE = "TC-003-025"
    DATA_FILE = "tc_003_025_data.csv"

    def test_tc_003_025_data_driven(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                moodle_quiz_prepare.prepare_multiple_choice_question_form(self, row)



if __name__ == "__main__":
    unittest.main()
