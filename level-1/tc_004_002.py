# -*- coding: utf-8 -*-
import unittest

import moodle_enrol_helpers as enrol
from moodle_test_base import MoodleDataDrivenTestCase


class TC_004_002_EnrolRoles(MoodleDataDrivenTestCase):
    DATA_FILE = "tc_004_002_data.csv"
    LOG_PREFIX = "TC-004-002"

    def test_enrol_with_different_roles(self):
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
                self.log_step("Search user")
                enrol.type_in_user_search(self, row["search_keyword"])
                self.log_step("Select role")
                enrol.select_role(self, row["role"])
                self.log_step("Select user")
                enrol.select_user_suggestion(self, row["user_name"])
                self.log_step("Enrol selected user")
                enrol.click_enrol_selected(self)
                self.log_step("Verify expected result")
                enrol.assert_pass_fail_result(self, row["expected_result"], row["user_name"])


if __name__ == "__main__":
    unittest.main()
