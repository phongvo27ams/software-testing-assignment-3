# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase


class TC_003_002_DataDriven(MoodleDataDrivenTestCase):
    TEST_CASE = "TC-003-002"
    DATA_FILE = "tc_003_002_data.csv"

    def test_tc_003_002_data_driven(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                moodle_quiz_prepare.prepare_logged_in_course_edit_mode(self, row)
                moodle_quiz_prepare.add_quiz_activity(self, row)



if __name__ == "__main__":
    unittest.main()
