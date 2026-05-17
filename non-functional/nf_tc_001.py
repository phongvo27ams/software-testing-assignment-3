# -*- coding: utf-8 -*-
import csv
import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
LEVEL_1_DIR = ROOT_DIR / "level-1"
sys.path.insert(0, str(LEVEL_1_DIR))

from moodle_test_base import MoodleDataDrivenTestCase
from selenium.webdriver.common.by import By


class PasswordFieldSecurityTest(MoodleDataDrivenTestCase):
    TEST_CASE = "NF-TC-001"
    DATA_FILE = "nf_tc_001_data.csv"
    LOG_PREFIX = "NF-TC-001"

    def read_data(self):
        data_file = Path(__file__).resolve().parent / "data" / self.DATA_FILE
        with open(data_file, newline="", encoding="utf-8-sig") as csv_file:
            return list(csv.DictReader(csv_file))

    def test_password_field_is_masked(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                self.log_step("Open login page")
                self.driver.get(row["login_url"])
                self.log_step("Verify password input type")
                password_field = self.wait_for_stable_element(By.ID, row["password_input_id"])
                self.assertEqual(
                    row["expected_type"],
                    password_field.get_attribute("type"),
                    "Security issue: password field is not masked.",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
