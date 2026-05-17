# -*- coding: utf-8 -*-
import csv
import sys
import time
import unittest
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
LEVEL_1_DIR = ROOT_DIR / "level-1"
sys.path.insert(0, str(LEVEL_1_DIR))

from moodle_test_base import MoodleDataDrivenTestCase
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class EnrolmentWorkflowPerformanceTest(MoodleDataDrivenTestCase):
    TEST_CASE = "NF-TC-004-001"
    DATA_FILE = "nf_tc_004_001_data.csv"
    LOG_PREFIX = "NF-TC-004-001"

    REPORT_DIR = Path(__file__).resolve().parent / "reports"

    def read_data(self):
        data_file = Path(__file__).resolve().parent / "data" / self.DATA_FILE
        with open(data_file, newline="", encoding="utf-8-sig") as csv_file:
            return list(csv.DictReader(csv_file))

    def setUp(self):
        super(EnrolmentWorkflowPerformanceTest, self).setUp()
        self.results = []
        self.REPORT_DIR.mkdir(exist_ok=True)

    def tearDown(self):
        self.write_report()
        super(EnrolmentWorkflowPerformanceTest, self).tearDown()

    def test_enrolment_workflow_performance(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                self.log_step("Measure login page load")
                self.measure(
                    "login_page_load",
                    float(row["max_login_page_load_seconds"]),
                    lambda: self.open_login_page(row),
                )

                self.log_step("Login as teacher")
                self.login(row)
                self.unenrol_if_enrolled(row)

                self.log_step("Measure participants page load")
                self.measure(
                    "participants_page_load",
                    float(row["max_participants_page_load_seconds"]),
                    lambda: self.open_participants_page(row),
                )

                self.log_step("Measure enrol dialog open")
                self.measure(
                    "enrol_dialog_open",
                    float(row["max_enrol_dialog_open_seconds"]),
                    lambda: self.open_enrol_dialog(row),
                )

                self.log_step("Measure autocomplete response")
                self.measure(
                    "autocomplete_response",
                    float(row["max_autocomplete_response_seconds"]),
                    lambda: self.search_user(row),
                )

                self.log_step("Measure enrol submission")
                self.measure(
                    "enrol_submission",
                    float(row["max_enrol_submission_seconds"]),
                    lambda: self.select_user_and_submit(row),
                )

    def measure(self, step, max_seconds, action):
        start = time.perf_counter()
        action()
        elapsed = time.perf_counter() - start
        status = "PASS" if elapsed <= max_seconds else "WARN"
        self.results.append(
            {
                "step": step,
                "elapsed_s": "%.3f" % elapsed,
                "sla_s": "%.3f" % max_seconds,
                "status": status,
            }
        )
        print(
            "[NF-TC-004-001] %-28s %.3fs / max %.3fs [%s]"
            % (step, elapsed, max_seconds, status),
            flush=True,
        )
        self.assertLessEqual(elapsed, max_seconds, "%s exceeded SLA" % step)

    def open_login_page(self, row):
        self.driver.get(row["login_url"])
        self.wait_for_stable_element(By.ID, row["login_button_id"])

    def open_participants_page(self, row):
        self.driver.get(row["participants_url"])
        self.wait_for_stable_element(By.XPATH, row["enrol_users_button_xpath"])

    def open_enrol_dialog(self, row):
        self.click(By.XPATH, row["enrol_users_button_xpath"])
        self.wait_for_stable_element(By.XPATH, row["search_box_xpath"])

    def search_user(self, row):
        search_box = self.wait_for_stable_element(By.XPATH, row["search_box_xpath"])
        search_box.click()
        search_box.clear()
        search_box.send_keys(row["search_keyword"])
        self.wait_for_stable_element(By.XPATH, row["user_suggestion_xpath"])

    def select_user_and_submit(self, row):
        self.click(By.XPATH, row["user_suggestion_xpath"])
        submit_button = self.wait_for_stable_element(By.XPATH, row["submit_enrol_button_xpath"])
        self.driver.execute_script("arguments[0].click();", submit_button)
        try:
            WebDriverWait(self.driver, 30).until(
                lambda driver: len(driver.find_elements(By.XPATH, row["submit_enrol_button_xpath"])) == 0
            )
        except TimeoutException:
            pass

    def unenrol_if_enrolled(self, row):
        self.driver.get(row["participants_url"])
        time.sleep(1)
        trash_buttons = self.driver.find_elements(By.XPATH, row["unenrol_button_xpath"])
        if not trash_buttons:
            return
        self.driver.execute_script("arguments[0].click();", trash_buttons[0])
        try:
            confirm = self.wait_for_stable_element(By.XPATH, row["unenrol_confirm_button_xpath"], timeout=8)
            self.driver.execute_script("arguments[0].click();", confirm)
            time.sleep(1)
        except TimeoutException:
            pass

    def write_report(self):
        if not getattr(self, "results", None):
            return
        report_path = self.REPORT_DIR / (
            "nf_tc_004_001_performance_%s.csv" % datetime.now().strftime("%Y%m%d_%H%M%S")
        )
        with open(report_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["step", "elapsed_s", "sla_s", "status"])
            writer.writeheader()
            writer.writerows(self.results)
        print("[NF-TC-004-001] Report saved: %s" % report_path, flush=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
