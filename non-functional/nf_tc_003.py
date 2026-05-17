# -*- coding: utf-8 -*-
import csv
import os
import sys
import time
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
LEVEL_1_DIR = ROOT_DIR / "level-1"
sys.path.insert(0, str(LEVEL_1_DIR))

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase
from selenium.webdriver.common.by import By


class MoodlePerformanceTest(MoodleDataDrivenTestCase):
    TEST_CASE = "PERF-001"
    DATA_FILE = "nf_tc_003_data.csv"
    LOG_PREFIX = "NF-TC-003"

    def read_data(self):
        data_file = Path(__file__).resolve().parent / "data" / self.DATA_FILE
        with open(data_file, newline="", encoding="utf-8-sig") as csv_file:
            return list(csv.DictReader(csv_file))

    def measure(self, label, max_seconds, action):
        start = time.perf_counter()
        action()
        elapsed = time.perf_counter() - start
        print("[Performance] %-35s %.2fs / max %.2fs" % (label, elapsed, max_seconds), flush=True)
        self.assertLessEqual(
            elapsed,
            max_seconds,
            "%s took %.2fs, expected <= %.2fs" % (label, elapsed, max_seconds),
        )
        return elapsed

    def test_moodle_quiz_creation_flow_performance(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                total_start = time.perf_counter()

                self.measure(
                    "Open Moodle home page",
                    float(row["max_open_home_seconds"]),
                    lambda: self.driver.get(row["site_url"]),
                )

                self.measure(
                    "Login",
                    float(row["max_login_seconds"]),
                    lambda: self.login(row),
                )

                self.measure(
                    "Open target course",
                    float(row["max_open_course_seconds"]),
                    lambda: self.click(By.XPATH, row["course_xpath"]),
                )

                def enable_edit_mode():
                    if not self.is_element_present(By.XPATH, row["insert_button_xpath"]):
                        self.click(By.XPATH, row["edit_mode_checkbox_xpath"])
                    self.wait_for_stable_element(By.XPATH, row["insert_button_xpath"], timeout=30)

                self.measure(
                    "Enable edit mode",
                    float(row["max_enable_edit_mode_seconds"]),
                    enable_edit_mode,
                )

                self.measure(
                    "Open New Quiz form",
                    float(row["max_open_quiz_form_seconds"]),
                    lambda: moodle_quiz_prepare.add_quiz_activity(self, row, verify_heading=True),
                )

                total_elapsed = time.perf_counter() - total_start
                print(
                    "[Performance] %-35s %.2fs / max %.2fs"
                    % ("Total flow", total_elapsed, float(row["max_total_seconds"])),
                    flush=True,
                )
                self.assertLessEqual(
                    total_elapsed,
                    float(row["max_total_seconds"]),
                    "Total flow took %.2fs, expected <= %.2fs"
                    % (total_elapsed, float(row["max_total_seconds"])),
                )


if __name__ == "__main__":
    unittest.main()
