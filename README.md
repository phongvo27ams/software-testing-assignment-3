# Mount Orange University Data-driven Automation Testing

This project contains Selenium WebDriver automation tests for Mount Orange University Moodle. The tests are written in Python `unittest` and organized into functional data-driven tests and non-functional tests.

The project includes:

- `level-1`: data-driven tests where input data and expected results are read from CSV files.
- `level-2`: data-driven tests where input data, expected results, URLs, locators, and other test items are externalized to CSV files.
- `non-functional`: security and performance tests for login, course creation, quiz creation, and enrolment workflows.

## Project Structure

```text
Assignment 3/
  README.md
  requirements.txt
  description.pdf

  level-1/
    data/
    moodle_test_base.py
    moodle_quiz_prepare.py
    moodle_enrol_helpers.py
    run_grouped_tests.py
    tc_001.py
    tc_002.py
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
    tc_004_001.py
    tc_004_002.py
    tc_004_003.py

  level-2/
    data/
    moodle_test_base.py
    moodle_quiz_prepare.py
    run_grouped_tests.py
    tc_001.py
    tc_002.py
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
    tc_004.py

  non-functional/
    data/
    reports/
    nf_tc_001.py
    nf_tc_002.py
    nf_tc_003.py
    nf_tc_004_001.py
    nf_tc_004_002.py
    run_nf_tests.py
```

## Requirements

- Windows
- Python 3.12
- Google Chrome or Chrome for Testing
- ChromeDriver matching the Chrome version
- Python packages from `requirements.txt`

Install dependencies:

```powershell
pip install -r requirements.txt
```

Current Python dependencies:

```text
selenium==3.141.0
urllib3==1.26.7
```

## Browser Setup

Download Chrome for Testing and ChromeDriver with the same major version. A recommended layout is:

```text
D:\Tools\chrome-win64\chrome.exe
D:\Tools\chromedriver-win64\chromedriver.exe
```

Set environment variables before running tests:

```powershell
$env:CHROME_DRIVER_PATH="D:\Tools\chromedriver-win64\chromedriver.exe"
$env:CHROME_BINARY_PATH="D:\Tools\chrome-win64\chrome.exe"
```

`CHROME_BINARY_PATH` is optional only when the installed system Chrome version matches ChromeDriver.

## Shared Helpers

- `moodle_test_base.py`: shared Chrome setup, CSV loading, login, click/type helpers, rich text editor helpers, select helpers, and common assertions.
- `moodle_quiz_prepare.py`: reusable quiz preconditions, such as opening a new quiz form or opening the Multiple choice question form.
- `moodle_enrol_helpers.py`: reusable enrolment helpers for Level 1 TC004 flows.
- `run_grouped_tests.py`: loads and runs all grouped functional test modules in a level folder.
- `run_nf_tests.py`: loads and runs all non-functional test modules.

## Level 1

Level 1 keeps browser actions and locators mostly in Python code. CSV files under `level-1/data` provide test input values and expected results.

Run all Level 1 grouped tests:

```powershell
python level-1\run_grouped_tests.py
```

Run one Level 1 test flow:

```powershell
python level-1\tc_001.py
python level-1\tc_002.py
python level-1\tc_003_003_005_006.py
python level-1\tc_003_011_013.py
python level-1\tc_003_030_039.py
python level-1\tc_004_001.py
python level-1\tc_004_002.py
python level-1\tc_004_003.py
```

## Level 2

Level 2 externalizes more test items into CSV. Besides input data and expected results, CSV files can contain URLs, locators, button IDs, expected-result locators, and expected UI states.

Run all Level 2 grouped tests:

```powershell
python level-2\run_grouped_tests.py
```

Run one Level 2 test flow:

```powershell
python level-2\tc_001.py
python level-2\tc_002.py
python level-2\tc_003_003_005_006.py
python level-2\tc_003_011_013.py
python level-2\tc_003_030_039.py
python level-2\tc_004.py
```

## Grouped Functional Test Flows

Similar manual test cases with the same workflow are grouped into one automation script. Each data row is executed as a `subTest`.

| Flow | Covered test cases | Description |
| --- | --- | --- |
| `tc_001.py` | TC001001 to TC001018 | Login validation |
| `tc_002.py` | TC002001 to TC002023 | Course creation validation |
| `tc_003_001.py` | TC-003-001 | Login, open course, enable edit mode |
| `tc_003_002.py` | TC-003-002 | Add Quiz activity |
| `tc_003_003_005_006.py` | TC-003-003, TC-003-005, TC-003-006 | Create quiz and verify quiz page |
| `tc_003_004.py` | TC-003-004 | Create quiz with description, time limit, grade, and password |
| `tc_003_007_010.py` | TC-003-007 to TC-003-010 | Quiz name validation and boundary testing |
| `tc_003_011_013.py` | TC-003-011 to TC-003-013 | Time limit validation |
| `tc_003_014_020.py` | TC-003-014 to TC-003-020 | Grade to pass validation |
| `tc_003_021_024.py` | TC-003-021 to TC-003-024 | Quiz password and Questions page validation |
| `tc_003_025.py` | TC-003-025 | Open Multiple choice question form |
| `tc_003_026_027.py` | TC-003-026 to TC-003-027 | Create valid Multiple choice questions |
| `tc_003_028_029.py` | TC-003-028 to TC-003-029 | Required-field validation for Multiple choice question |
| `tc_003_030_039.py` | TC-003-030 to TC-003-039 | Default mark, choices, and answer fraction validation |
| `level-1/tc_004_001.py` | TC004001 to TC004006 | Enrol user with date configurations |
| `level-1/tc_004_002.py` | TC004009 to TC004010 | Enrol user with different roles |
| `level-1/tc_004_003.py` | TC004007, TC004008, TC004011 to TC004013 | Enrol user search variations |
| `level-2/tc_004.py` | TC004001 to TC004010 | Fully externalized enrolment workflow using config, locators, and data CSV files |

## Non-functional Tests

Implemented non-functional test cases:

| Script | Type | Description |
| --- | --- | --- |
| `nf_tc_001.py` | Security | Verify that the login password field is masked |
| `nf_tc_002.py` | Performance | Verify that the course creation page loads within threshold |
| `nf_tc_003.py` | Performance | Measure the main Moodle quiz creation flow |
| `nf_tc_004_001.py` | Performance | Measure the enrolment workflow and write a CSV report |
| `nf_tc_004_002.py` | Security | Test enrolment search input against XSS, SQL injection, HTML injection, and sensitive error leakage |

Run all non-functional tests:

```powershell
python non-functional\run_nf_tests.py
```

Run one non-functional test:

```powershell
python non-functional\nf_tc_001.py
python non-functional\nf_tc_002.py
python non-functional\nf_tc_003.py
python non-functional\nf_tc_004_001.py
python non-functional\nf_tc_004_002.py
```

Non-functional data files are stored under:

```text
non-functional\data\
```

Performance reports are written to:

```text
non-functional\reports\
```

## Expected Output

`unittest` output uses standard markers:

- `.` means a test/subtest passed.
- `F` means assertion failure.
- `E` means runtime error.
- `OK` means the selected suite completed successfully.

Chrome may print internal warnings such as GCM, EGL, WebGPU, or sandbox messages. These messages are not test failures if `unittest` reports `OK`.

## Notes

- Each grouped script represents one automation test case for one shared workflow.
- Most grouped scripts restart the browser between data rows to keep rows independent and stable.
- The tests run against the public Moodle demo site, so response time and page state can vary.
- If ChromeDriver and Chrome versions do not match, Selenium may fail before any test step starts. Use matching Chrome for Testing and ChromeDriver versions.
- If Git reports `dubious ownership`, run:

```powershell
git config --global --add safe.directory "D:/Documents/Computer Science/Software Testing/Assignment/Assignment 3"
```
