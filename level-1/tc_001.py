# -*- coding: utf-8 -*-
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from moodle_test_base import MoodleDataDrivenTestCase


class TC_001_LoginDataDriven(MoodleDataDrivenTestCase):
    DATA_FILE = "tc_001_data.csv"
    LOG_PREFIX = "TC-001"
    LOGIN_URL = "https://school.moodledemo.net/login/index.php"

    def test_login_data_driven(self):
        for index, row in enumerate(self.rows()):
            if index > 0:
                self.restart_driver()

            with self.subTest(row["test_id"]):
                self.log_step("Open login page")
                self.driver.get(self.LOGIN_URL)

                self.log_step("Enter username and password")
                self.type_text(By.ID, "username", row["username"])
                self.type_text(By.ID, "password", row["password"])

                self.log_step("Submit login form")
                username_input = self.wait_for_stable_element(By.ID, "username")
                password_input = self.wait_for_stable_element(By.ID, "password")
                login_button = self.wait_for_stable_element(By.ID, "loginbtn")
                self.driver.execute_script(
                    """
                    arguments[0].value = arguments[3];
                    arguments[1].value = arguments[4];
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[1].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    arguments[1].dispatchEvent(new Event('change', { bubbles: true }));
                    arguments[2].click();
                    """,
                    username_input,
                    password_input,
                    login_button,
                    row["username"],
                    row["password"],
                )

                self.log_step("Verify expected login result")
                expected = self.wait_for_stable_element(By.XPATH, row["xpath_to_verify"], timeout=30)
                self.assertEqual(row["expected_text"], expected.text)

                if row.get("should_logout", "").upper() == "TRUE":
                    self.logout_if_possible()

    def logout_if_possible(self):
        self.driver.get("https://school.moodledemo.net/login/logout.php")
        try:
            continue_button = WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element(By.XPATH, "//button[contains(normalize-space(.), 'Continue')]")
            )
            continue_button.click()
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()
