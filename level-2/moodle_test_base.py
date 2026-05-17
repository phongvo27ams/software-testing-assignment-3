# -*- coding: utf-8 -*-
import csv
import os
import tempfile
import unittest

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class MoodleDataDrivenTestCase(unittest.TestCase):
    TEST_CASE = ""
    DATA_FILE = ""
    LOG_PREFIX = ""

    def setUp(self):
        self.driver = self.create_driver()

    def tearDown(self):
        self.driver.quit()

    def restart_driver(self):
        self.driver.quit()
        self.driver = self.create_driver()

    def create_driver(self):
        driver_path = os.environ.get("CHROME_DRIVER_PATH", "")
        chrome_binary_path = os.environ.get("CHROME_BINARY_PATH", "")
        if not chrome_binary_path and driver_path:
            chrome_binary_path = os.path.join(
                os.path.dirname(os.path.dirname(driver_path)),
                "chrome-win64",
                "chrome.exe",
            )

        options = Options()
        options.add_argument("--incognito")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--user-data-dir=%s" % tempfile.mkdtemp(prefix=self.profile_prefix()))
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-component-update")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-features=MediaRouter,OptimizationHints,Translate,AutofillServerCommunication")
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "autofill.profile_enabled": False,
                "autofill.credit_card_enabled": False,
                "profile.default_content_setting_values.notifications": 2,
            },
        )
        if chrome_binary_path and os.path.exists(chrome_binary_path):
            options.binary_location = chrome_binary_path

        if driver_path:
            try:
                driver = webdriver.Chrome(executable_path=driver_path, options=options)
            except TypeError:
                driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        else:
            try:
                driver = webdriver.Chrome(options=options)
            except TypeError:
                driver = webdriver.Chrome(chrome_options=options)

        driver.implicitly_wait(10)
        driver.set_page_load_timeout(60)
        driver.maximize_window()
        return driver

    def profile_prefix(self):
        return "%s_" % self.TEST_CASE.lower().replace("-", "_")

    def log_step(self, message):
        prefix = self.LOG_PREFIX or self.TEST_CASE or self.__class__.__name__
        print("[%s] %s" % (prefix, message), flush=True)

    def read_data(self):
        data_file = os.path.join(os.path.dirname(__file__), "data", self.DATA_FILE)
        with open(data_file, newline="", encoding="utf-8-sig") as csv_file:
            return list(csv.DictReader(csv_file))

    def rows(self):
        for row in self.read_data():
            if not self.TEST_CASE or row["test_case"] == self.TEST_CASE:
                yield row

    def wait_for_stable_element(self, by, locator, timeout=30):
        def find_element(driver):
            try:
                element = driver.find_element(by=by, value=locator)
                element.is_enabled()
                return element
            except StaleElementReferenceException:
                return False

        return WebDriverWait(self.driver, timeout).until(find_element)

    def click(self, by, locator, timeout=30):
        element = self.wait_for_stable_element(by, locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
        return element

    def click_first_available_xpath(self, locators, timeout=30):
        last_error = None
        for locator in locators:
            try:
                return self.click(By.XPATH, locator, timeout=timeout)
            except Exception as error:
                last_error = error
        raise last_error

    def type_text(self, by, locator, value):
        last_error = None
        for _ in range(3):
            try:
                element = self.wait_for_stable_element(by, locator)
                element.click()
                element.clear()
                element.send_keys(value or "")
                return element
            except StaleElementReferenceException as error:
                last_error = error
        raise last_error

    def set_input_value(self, by, locator, value):
        element = self.wait_for_stable_element(by, locator)
        self.driver.execute_script(
            """
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            value or "",
        )
        return element

    def type_text_or_set_value(self, by, locator, value):
        try:
            return self.type_text(by, locator, value)
        except ElementNotInteractableException:
            return self.set_input_value(by, locator, value)

    def set_editor_text_by_data_id(self, data_id, value):
        locator = '//*[@data-id="%s"]' % data_id
        element = self.find_editor_element(locator, data_id)
        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({block: 'center'});
            arguments[0].focus();
            if ('value' in arguments[0]) {
                arguments[0].value = arguments[1];
            } else {
                arguments[0].innerHTML = arguments[1];
                arguments[0].textContent = arguments[1];
            }
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            element,
            value or "",
        )
        self.driver.switch_to.default_content()
        return element

    def find_editor_element(self, locator, data_id):
        try:
            self.driver.switch_to.default_content()
            return self.wait_for_stable_element(By.XPATH, locator, timeout=5)
        except TimeoutException:
            pass

        frames = self.driver.find_elements_by_tag_name("iframe")
        for frame in frames:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(frame)
            try:
                return self.wait_for_stable_element(By.XPATH, locator, timeout=3)
            except TimeoutException:
                continue

        self.driver.switch_to.default_content()
        for fallback_id in (data_id, "%seditable" % data_id):
            try:
                return self.wait_for_stable_element(By.ID, fallback_id, timeout=3)
            except TimeoutException:
                continue

        raise AssertionError("Could not find editor element for data-id: %s" % data_id)

    def select_option_by_visible_text(self, select_id, text):
        select = self.wait_for_stable_element(By.ID, select_id)
        self.driver.execute_script(
            """
            const select = arguments[0];
            const label = arguments[1];
            for (const option of select.options) {
                if (option.text.trim() === label) {
                    select.value = option.value;
                    break;
                }
            }
            select.dispatchEvent(new Event('input', { bubbles: true }));
            select.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            select,
            text,
        )
        return select

    def is_element_present(self, by, locator):
        try:
            self.driver.find_element(by=by, value=locator)
        except NoSuchElementException:
            return False
        return True

    def login(self, row):
        if self.is_logged_in():
            self.log_step("Already logged in")
            return

        self.log_step("Open login page")
        self.driver.get(row["login_url"])

        if not self.wait_for_login_form_or_session(timeout=12):
            self.driver.get(row["site_url"])
            if self.wait_for_logged_in(timeout=8):
                self.log_step("Already logged in")
                return

        if self.is_logged_in():
            self.log_step("Already logged in")
            return

        self.log_step("Enter username and password")
        self.type_text(By.ID, "username", row["username"])
        self.type_text(By.ID, "password", row["password"])

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
        WebDriverWait(self.driver, 20).until(
            lambda driver: "login/index.php" not in driver.current_url
            or self.is_element_present(By.CSS_SELECTOR, "#loginerrormessage, .loginerrors, .alert-danger")
        )
        self.assertNotIn("login/index.php", self.driver.current_url, "Login failed; still on login page.")

    def is_logged_in(self):
        return self.is_element_present(By.ID, "user-menu-toggle") or self.is_element_present(
            By.CSS_SELECTOR,
            "[data-region='user-menu']",
        )

    def wait_for_logged_in(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver: self.is_logged_in())
            return True
        except TimeoutException:
            return False

    def wait_for_login_form_or_session(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: self.is_element_present(By.ID, "username") or self.is_logged_in()
            )
            return True
        except TimeoutException:
            return False

    def ensure_checkbox_checked(self, checkbox_id):
        checkbox = self.wait_for_stable_element(By.ID, checkbox_id)
        if not checkbox.is_selected():
            self.click(By.ID, checkbox_id)

    def type_rich_text_html(self, aria_label, html):
        xpath = "//*[@aria-label=%r]" % aria_label
        try:
            editor = self.wait_for_stable_element(By.XPATH, xpath, timeout=10)
            self.set_editor_html(editor, html)
            return
        except TimeoutException:
            pass

        frames = self.driver.find_elements_by_tag_name("iframe")
        for frame in frames:
            self.driver.switch_to.frame(frame)
            try:
                editor = self.wait_for_stable_element(By.XPATH, xpath, timeout=3)
                self.set_editor_html(editor, html)
                self.driver.switch_to.default_content()
                return
            except Exception:
                self.driver.switch_to.default_content()

        raise AssertionError("Could not find rich text editor with aria-label: %s" % aria_label)

    def set_editor_html(self, editor, html):
        self.driver.execute_script(
            """
            arguments[0].focus();
            arguments[0].innerHTML = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """,
            editor,
            html,
        )

    def assert_expected_result(self, row):
        expected_type = row["expected_type"]
        if expected_type in ("questionname", "text"):
            element = self.wait_for_stable_element(By.XPATH, row["expected_xpath"])
            self.assertEqual(row["expected_text"], element.text)
        elif expected_type == "heading":
            self.click(By.XPATH, row["questions_nav_xpath"])
            heading = self.wait_for_stable_element(By.XPATH, row["expected_heading_xpath"])
            self.assertEqual(row["expected_text"], heading.text)
        elif expected_type == "body_not_contains":
            self.assertNotIn(row["expected_text"], self.driver.find_element_by_css_selector("BODY").text)
        elif expected_type in ("error_id", "error_text"):
            error = self.wait_for_stable_element(By.ID, row["expected_error_id"])
            self.assertEqual(self.normalize_text(row["expected_text"]), self.normalize_text(error.text))
        elif expected_type == "error_xpath":
            error = self.wait_for_stable_element(By.XPATH, row["expected_xpath"])
            self.assertIn(self.normalize_text(row["expected_text"]), self.normalize_text(error.text))
        else:
            raise AssertionError("Unsupported expected_type: %s" % expected_type)

    def normalize_text(self, value):
        return " ".join((value or "").split())
