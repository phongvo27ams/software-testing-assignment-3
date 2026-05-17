# -*- coding: utf-8 -*-
import unittest

import moodle_quiz_prepare
from moodle_test_base import MoodleDataDrivenTestCase


class PrepareMCQQuestionForm(MoodleDataDrivenTestCase):
    TEST_CASE = "PREP-MCQ-QUESTION-FORM"
    DATA_FILE = "prepare_mcq_question_form_data.csv"

    def test_prepare_multiple_choice_question_form(self):
        for row in self.rows():
            with self.subTest(row["test_case"]):
                moodle_quiz_prepare.prepare_multiple_choice_question_form(self, row)


if __name__ == "__main__":
    unittest.main()
