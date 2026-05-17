# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


def prepare_logged_in_course_edit_mode(test_case, row):
    test_case.log_step("Open Moodle home")
    test_case.driver.get(row["site_url"])
    test_case.login(row)

    test_case.log_step("Open course")
    test_case.click(By.XPATH, row["course_xpath"])

    if not test_case.is_element_present(By.XPATH, row["insert_button_xpath"]):
        test_case.log_step("Enable edit mode")
        test_case.click(By.XPATH, row["edit_mode_checkbox_xpath"])
        test_case.wait_for_stable_element(By.XPATH, row["insert_button_xpath"], timeout=30)


def add_quiz_activity(test_case, row, verify_heading=True):
    test_case.log_step("Click Add content")
    test_case.click(By.XPATH, row["add_content_button_xpath"])

    test_case.log_step("Click Add an activity or resource")
    test_case.click(By.XPATH, row["add_activity_button_xpath"])

    test_case.log_step("Click Add a new Quiz")
    test_case.click(By.XPATH, row["quiz_link_xpath"])

    test_case.log_step("Click Add selected activity")
    test_case.click_first_available_xpath(
        [
            row["add_selected_button_xpath"],
            "//button[contains(normalize-space(.), 'Add selected activity')]",
            "//button[contains(normalize-space(.), 'Add selected')]",
            "//button[contains(@title, 'Add selected')]",
            "//button[@data-action='save' or @data-action='submit' or @data-action='add']",
            "//div[contains(@class, 'modal-footer')]//button[contains(@class, 'btn-primary') and not(@disabled)]",
            "//div[contains(@class, 'modal-footer')]//input[@type='submit' and not(@disabled)]",
        ],
        timeout=10,
    )

    if verify_heading:
        test_case.log_step("Verify New Quiz heading")
        h2 = test_case.wait_for_stable_element(By.XPATH, row["expected_h2_xpath"])
        test_case.assertEqual(row["expected_h2_text"], h2.text)


def prepare_new_quiz_form(test_case, row, verify_heading=False):
    prepare_logged_in_course_edit_mode(test_case, row)
    add_quiz_activity(test_case, row, verify_heading=verify_heading)


def prepare_quiz_questions_page(test_case, row):
    prepare_new_quiz_form(test_case, row, verify_heading=False)

    test_case.log_step("Enter quiz name")
    test_case.type_text(By.ID, row.get("name_input_id", "id_name"), row.get("quiz_name", "Quiz 1"))

    test_case.log_step("Save and display")
    test_case.click(By.XPATH, row.get("save_button_xpath", '//input[@value="Save and display"]'))

    test_case.log_step("Open Questions page")
    test_case.click(
        By.XPATH,
        row.get(
            "questions_nav_xpath",
            '//li[@data-key="mod_quiz_edit"]',
        ),
    )


def prepare_multiple_choice_question_form(test_case, row):
    prepare_quiz_questions_page(test_case, row)

    test_case.log_step("Click Add question menu")
    test_case.click(
        By.XPATH,
        row.get(
            "question_add_menu_xpath",
            '//span[contains(concat(" ", normalize-space(@class), " "), " add-menu ") and normalize-space(.)="Add"]',
        ),
    )

    test_case.log_step("Click a new question")
    test_case.click(
        By.XPATH,
        row.get(
            "new_question_xpath",
            '//span[contains(concat(" ", normalize-space(@class), " "), " menu-action-text ") and normalize-space(.)="a new question"]',
        ),
    )

    test_case.log_step("Select Multiple choice")
    test_case.click(
        By.XPATH,
        row.get(
            "multiple_choice_type_xpath",
            '//span[contains(concat(" ", normalize-space(@class), " "), " typename ") and normalize-space(.)="Multiple choice"]',
        ),
    )

    test_case.log_step("Click Add")
    test_case.click(
        By.XPATH,
        row.get(
            "add_question_type_button_xpath",
            '//input[@type="submit" and @value="Add"]',
        ),
    )

    test_case.log_step("Verify Adding a Multiple choice question heading")
    h2 = test_case.wait_for_stable_element(
        By.XPATH,
        row.get(
            "expected_h2_xpath",
            '//h2[normalize-space(.)="Adding a Multiple choice question"]',
        ),
    )
    test_case.assertEqual(
        row.get("expected_h2_text", "Adding a Multiple choice question"),
        h2.text,
    )
