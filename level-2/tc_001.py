# -*- coding: utf-8 -*-
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from moodle_test_base import MoodleDataDrivenTestCase


class TC_001_LoginDataDrivenLevel2(MoodleDataDrivenTestCase):
    DATA_FILE = "tc_001_data.csv"
    LOG_PREFIX = "L2-TC-001"
    LOGOUT_URL = "https://school.moodledemo.net/login/logout.php"

    def test_login_data_driven(self):
        for index, row in enumerate(self.read_data()):
            if index > 0:
                self.restart_driver()
            with self.subTest(row["test_id"]):
                self.log_step("Open login page")
                self.open_clean_login_page(row)
                self.log_step("Enter username and password")
                self.type_text(By.ID, row["username_id"], row["username"])
                self.type_text(By.ID, row["password_id"], row["password"])
                self.click(By.ID, row["loginbtn_id"])
                self.log_step("Verify expected result")
                self.verify_login_result(row)
                if row["should_logout"].strip().upper() == "TRUE":
                    self.logout_if_needed()

    def open_clean_login_page(self, row):
        self.driver.get(self.LOGOUT_URL)
        if "logout.php" in self.driver.current_url:
            try:
                self.click(By.XPATH, "//button[contains(.,'Continue')]", timeout=3)
            except Exception:
                pass
        self.driver.get(row["url"])
        self.wait_for_stable_element(By.ID, row["loginbtn_id"])

    def verify_login_result(self, row):
        element = self.wait_for_stable_element(By.XPATH, row["xpath_to_verify"])
        self.assertEqual(
            self.normalize_text(row["expected_text"]),
            self.normalize_text(element.text),
        )

    def logout_if_needed(self):
        self.driver.get(self.LOGOUT_URL)
        try:
            self.click(By.XPATH, "//button[contains(.,'Continue')]", timeout=3)
            WebDriverWait(self.driver, 5).until(lambda driver: "logout.php" not in driver.current_url)
        except TimeoutException:
            pass
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
