# Non-functional Testing - Performance

This folder contains one automated non-functional test for Moodle performance.

## Testing Type

Performance Testing

## Objective

Measure whether the main Moodle quiz creation flow completes within acceptable response-time thresholds.

The automated flow measures:

- Open Moodle home page
- Login
- Open target course
- Enable edit mode
- Open the New Quiz form
- Total flow duration

## Tool

- Python `unittest`
- Selenium WebDriver
- ChromeDriver
- Python `time.perf_counter()`

## Test Data

Performance thresholds and UI test items are stored in:

```text
non-functional/data/performance_test_data.csv
```

## Browser Setup

```powershell
$env:CHROME_DRIVER_PATH="D:\Tools\chromedriver-win64\chromedriver.exe"
$env:CHROME_BINARY_PATH="D:\Tools\chrome-win64\chrome.exe"
```

## Run

From the project root:

```powershell
python non-functional\performance_test.py
```

## Pass Criteria

The test passes when every measured step is less than or equal to the configured threshold in the CSV file.
