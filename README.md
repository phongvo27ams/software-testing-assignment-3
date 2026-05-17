# Moodle Data-driven Automation Testing

This project contains Python Selenium `unittest` automation scripts for Mount Orange University Moodle test cases from Project #2.

The project includes:

- `level-1`: data-driven automation testing. Test input data and expected results are read from CSV files.
- `level-2`: data-driven automation testing where both test data and test items are read from CSV files. Test items include URLs, input locators, button locators, expected-result locators, and expected UI states.
- `non-functional`: automated Performance Testing for the main Moodle quiz creation flow.

## Project Structure

```text
Assignment 3/
  requirements.txt
  description.pdf
  README.md
  level-1/
    data/
    moodle_test_base.py
    moodle_quiz_prepare.py
    run_grouped_tests.py
    tc_001.py
    tc_003_001.py
    tc_003_002.py
    tc_003_003_005_006.py
    tc_003_004.py
    tc_003_007_010.py
    tc_003_011_013.py
    tc_003_014_020.py
    tc_003_021_024.py
    tc_003_025.py
    tc_003_026_027.py
    tc_003_028_029.py
    tc_003_030_039.py
  level-2/
    data/
    moodle_test_base.py
    moodle_quiz_prepare.py
    run_grouped_tests.py
    tc_003_001.py
    tc_003_002.py
    tc_003_003_005_006.py
    tc_003_004.py
    tc_003_007_010.py
    tc_003_011_013.py
    tc_003_014_020.py
    tc_003_021_024.py
    tc_003_025.py
    tc_003_026_027.py
    tc_003_028_029.py
    tc_003_030_039.py
  non-functional/
    data/
    performance_test.py
```

## Common Helpers

- `moodle_test_base.py`: shared Selenium setup, CSV loading, login, click/type helpers, rich text editor helpers, select helpers, and common assertions.
- `moodle_quiz_prepare.py`: reusable Moodle preconditions, such as opening a new quiz form or opening the Multiple choice question form.
- `run_grouped_tests.py`: runs the grouped automation test cases.

## Requirements

- Windows
- Python 3.12
- Google Chrome for Testing
- ChromeDriver matching the Chrome for Testing version
- Python packages listed in `requirements.txt`

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Current dependencies:

```text
selenium==3.141.0
urllib3==1.26.7
```

## Browser Setup

Download and extract Chrome for Testing and ChromeDriver. A recommended local layout is:

```text
D:\Tools\chrome-win64\chrome.exe
D:\Tools\chromedriver-win64\chromedriver.exe
```

Set environment variables before running tests:

```powershell
$env:CHROME_DRIVER_PATH="D:\Tools\chromedriver-win64\chromedriver.exe"
$env:CHROME_BINARY_PATH="D:\Tools\chrome-win64\chrome.exe"
```

`CHROME_BINARY_PATH` is optional only when your system Chrome version matches ChromeDriver.

## Grouped Test Flows

Similar manual test cases with the same workflow are grouped into one automation script. Each grouped script reads multiple rows from CSV and runs each row as a `subTest`.

| Script | Covered test cases | Main flow |
| --- | --- | --- |
| `level-1/tc_001.py` | TC001001 to TC001018 | Login validation with valid and invalid accounts |
| `tc_003_001.py` | TC-003-001 | Login, open course, enable edit mode |
| `tc_003_002.py` | TC-003-002 | Add Quiz activity |
| `tc_003_003_005_006.py` | TC-003-003, TC-003-005, TC-003-006 | Create quiz and verify quiz page |
| `tc_003_004.py` | TC-003-004 | Create quiz with description, time limit, grade, password |
| `tc_003_007_010.py` | TC-003-007 to TC-003-010 | Quiz name validation and boundary testing |
| `tc_003_011_013.py` | TC-003-011 to TC-003-013 | Time limit validation |
| `tc_003_014_020.py` | TC-003-014 to TC-003-020 | Grade to pass validation |
| `tc_003_021_024.py` | TC-003-021 to TC-003-024 | Quiz password and Questions page |
| `tc_003_025.py` | TC-003-025 | Open Multiple choice question form |
| `tc_003_026_027.py` | TC-003-026 to TC-003-027 | Create valid Multiple choice questions |
| `tc_003_028_029.py` | TC-003-028 to TC-003-029 | Required-field validation for Multiple choice question |
| `tc_003_030_039.py` | TC-003-030 to TC-003-039 | Default mark, choices, and answer fraction validation |

## Run Level 1

Run all grouped Level 1 test cases:

```powershell
python level-1\run_grouped_tests.py
```

Run one grouped Level 1 flow:

```powershell
python level-1\tc_001.py
python level-1\tc_003_003_005_006.py
python level-1\tc_003_011_013.py
python level-1\tc_003_030_039.py
```

## Run Level 2

Level 2 uses the same grouped workflows as Level 1, but CSV files under `level-2/data` contain both testing data and testing items such as URLs and locators.

Run all grouped Level 2 test cases:

```powershell
python level-2\run_grouped_tests.py
```

Run one grouped Level 2 flow:

```powershell
python level-2\tc_003_003_005_006.py
python level-2\tc_003_011_013.py
python level-2\tc_003_030_039.py
```

## Non-functional Testing - Performance

Testing type: Performance Testing.

Objective: measure whether the main Moodle quiz creation flow completes within acceptable response-time thresholds.

The automated performance flow measures:

- Open Moodle home page
- Login
- Open target course
- Enable edit mode
- Open the New Quiz form
- Total flow duration

Tool:

- Python `unittest`
- Selenium WebDriver
- ChromeDriver
- Python `time.perf_counter()`

Performance thresholds and UI test items are stored in:

```text
non-functional\data\performance_test_data.csv
```

Run the performance test:

```powershell
python non-functional\performance_test.py
```

Pass criteria: every measured step must be less than or equal to the configured threshold in the CSV file.

## Notes

- Each grouped script is one automation test case for one shared workflow.
- For grouped scripts, each row restarts the browser after the first row to keep rows independent and stable.
- Chrome may print internal warnings such as GCM, EGL, or sandbox messages. If `unittest` still reports `OK`, those Chrome messages are not test failures.
- `.` in unittest output means one test passed. `OK` is printed after the whole selected suite finishes.
