# -*- coding: utf-8 -*-
import unittest

import moodle_enrol_helpers as enrol
from moodle_test_base import MoodleDataDrivenTestCase


class TC_004_001_EnrolDates(MoodleDataDrivenTestCase):
    DATA_FILE = "tc_004_001_data.csv"
    LOG_PREFIX = "TC-004-001"

    def test_enrol_with_date_configurations(self):
        for index, row in enumerate(self.rows()):
            if index > 0:
                self.restart_driver()
            with self.subTest(row["tc_id"]):
                self.log_step("Login as teacher")
                enrol.login_as_teacher(self)
                self.log_step("Clean existing enrolment")
                enrol.unenrol_if_enrolled(self, row["user_name"])
                self.log_step("Open enrol users dialog")
                enrol.open_enrol_dialog(self)
                self.log_step("Search and select user")
                enrol.search_and_select_user(self, row["search_keyword"], row["user_name"])
                self.log_step("Set enrolment dates")
                enrol.set_enrol_dates(self, row)
                self.log_step("Enrol selected user")
                enrol.click_enrol_selected(self)
                self.log_step("Verify expected result")
                enrol.assert_pass_fail_result(self, row["expected_result"], row["user_name"])


if __name__ == "__main__":
    unittest.main()
