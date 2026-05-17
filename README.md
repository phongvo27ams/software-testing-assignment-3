# Moodle Data-driven Automation Testing

This project contains Python Selenium `unittest` automation scripts for Mount Orange University test cases from Project #2.

The project is organized into two automation levels:

- `level-1`: data-driven automation testing. Test input data and expected results are read from CSV files.
- `level-2`: data-driven automation testing where both test data and test items are read from CSV files. Test items include URLs, input locators, button locators, and expected-result locators.

## Project Structure

```text
Assignment 3/
  requirements.txt
  description.pdf
  level-1/
    data/
    moodle_test_base.py
    moodle_quiz_prepare.py
    run_all_tests.py
    tc_003_001.py ... tc_003_039.py
  level-2/
    data/
    moodle_test_base.py
    moodle_quiz_prepare.py
    run_all_tests.py
    tc_003_001.py ... tc_003_039.py
  non-functional/
    data/
    performance_test.py
```

Common helper files:

- `moodle_test_base.py`: shared Selenium setup, CSV loading, login, click/type helpers, rich text editor helpers, select helpers, and common assertions.
- `moodle_quiz_prepare.py`: reusable Moodle preconditions, such as opening a new quiz form or opening the Multiple choice question form.
- `run_all_tests.py`: runs all test cases in order, or a selected range.

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

## Run Level 1

Run all Level 1 test cases:

```powershell
python level-1\run_all_tests.py
```

Run a selected range:

```powershell
python level-1\run_all_tests.py --start 25 --end 39 -v
```

Run one test case:

```powershell
python level-1\tc_003_001.py
```

## Run Level 2

Run all Level 2 test cases:

```powershell
python level-2\run_all_tests.py
```

Run a selected range:

```powershell
python level-2\run_all_tests.py --start 25 --end 39 -v
```

Run one test case:

```powershell
python level-2\tc_003_001.py
```

## Run Non-functional Performance Test

Run the Moodle performance test:

```powershell
python non-functional\performance_test.py
```

The performance thresholds are stored in:

```text
non-functional\data\performance_test_data.csv
```

## Notes

- Each test opens a fresh browser session, runs independently, and closes the browser after completion.
- Chrome may print internal warnings such as GCM or sandbox messages. If `unittest` still reports `OK`, those Chrome messages are not test failures.
- `.` in unittest output means one test passed. `OK` is printed after the whole selected suite finishes.
