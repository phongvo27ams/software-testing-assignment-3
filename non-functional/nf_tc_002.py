# -*- coding: utf-8 -*-
import csv
import sys
import time
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
LEVEL_1_DIR = ROOT_DIR / "level-1"
sys.path.insert(0, str(LEVEL_1_DIR))

from moodle_test_base import MoodleDataDrivenTestCase
from selenium.webdriver.common.by import By


class CourseCreationPageLoadPerformanceTest(MoodleDataDrivenTestCase):
    TEST_CASE = "NF-TC-002"
    DATA_FILE = "nf_tc_002_data.csv"
    LOG_PREFIX = "NF-TC-002"

    def read_data(self):
        data_file = Path(__file__).resolve().parent / "data" / self.DATA_FILE
        with open(data_file, newline="", encoding="utf-8-sig") as csv_file:
            return list(csv.DictReader(csv_file))

    def test_course_creation_page_load_time(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                self.log_step("Login as manager")
                self.login(row)
                self.log_step("Measure course creation page load")
                start = time.perf_counter()
                self.driver.get(row["course_url"])
                self.wait_for_stable_element(By.ID, row["expected_element_id"])
                elapsed = time.perf_counter() - start
                max_seconds = float(row["max_load_seconds"])
                print(
                    "[NF-TC-002] Course creation page loaded in %.2fs / max %.2fs"
                    % (elapsed, max_seconds),
                    flush=True,
                )
                self.assertLessEqual(
                    elapsed,
                    max_seconds,
                    "Course creation page took %.2fs, expected <= %.2fs" % (elapsed, max_seconds),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
