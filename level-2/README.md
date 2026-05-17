# Level 2 - Data-driven Test Cases and Test Items

Level 2 keeps both testing data and testing items in data files.

Compared with Level 1, the script should avoid hard-coding important UI items such as:

- Site URLs
- Page URLs
- Input locators
- Button locators
- Expected UI states or expected result locators

## Structure

- `moodle_test_base.py`: shared Selenium setup and common actions.
- `moodle_quiz_prepare.py`: reusable Moodle preconditions.
- `data/*.csv`: test data plus test items such as URLs and locators.
- `tc_003_*.py`: compact scripts that read test data and test items from CSV.

## Browser Setup

```powershell
$env:CHROME_DRIVER_PATH="D:\Tools\chromedriver-win64\chromedriver.exe"
$env:CHROME_BINARY_PATH="D:\Tools\chrome-win64\chrome.exe"
```

## Run

```powershell
python level-2\tc_003_001.py
```

Run all Level 2 test cases:

```powershell
python level-2\run_all_tests.py
```

Run a range:

```powershell
python level-2\run_all_tests.py --start 25 --end 39 -v
```
