# How to Test the Results

## Overview
This test verifies that recurring events are generated correctly. It ensures events occur on expected dates, tracks the number of events per week, and compares actual vs. expected results. Three data sources are used:
- **`existing_events_df`** – Current event definitions.
- **`test_cases_data_df`** – Expected parameters for test cases.
- **`test_results_df`** – Actual results from `count_weekly_events`.

---

## 1. Verify Event Occurrences
**Function:** `occurs_on`

### Steps
1. **Check event dates (using `existing_events_df`)**:
   - Ensure each event appears on the correct dates.
   - Example: A weekly event on Mondays should happen every 7 days, always on a Monday.

2. **Validate test case parameters (using `test_cases_data_df`)**:
   - **For n-weekly events:**
     - Ensure they repeat every `n * 7` days.
     - If an event occurs multiple times a week, treat each occurrence separately.

   - **For monthly events:**
     - Check that they occur on the correct day(s) of the month.
     - If a day doesn’t exist in a given month (e.g., 31st in February), confirm behavior:
       - **If `use_last_day` = True**, the event moves to the last valid day.
       - **If `use_last_day` = False**, the event is ignored that month.

✅ **Pass if:** Events occur on expected dates.
❌ **Fail if:** Missing or extra occurrences are found.

---

## 2a. Verify Weekly Event Counts
**Function:** `count_weekly_events`

### Steps
1. **Count weekly events (using `test_results_df`)**:
   - Identify the Monday that starts each week.
   - Count the total number of events in each week.
   - Store the results in a `weekly_count` table with:
     - **Week start date**
     - **Number of events that week**

✅ **Pass if:** Weekly counts match expectations.
❌ **Fail if:** Counts are incorrect (too many or too few events).

---

## 2b. Validate Test Case Results
Once event dates and weekly counts are confirmed, check if the test results match expectations.

### How Test Cases Work
- **Existing Events (`existing_events_df`)**: Contains known valid event parameters.
- **Test Cases (`test_cases_data_df`)**: Defines expected behaviors.
- **Test Results (`test_results_df`)**: Stores actual occurrences after running `count_weekly_events`.

### Steps
#### 1. Check if events repeat correctly (using `test_results_df` and `test_cases_data_df`)
- **For n-weekly events:**
  - Ensure the first occurrence appears in the correct starting week.
  - Confirm events repeat at the correct interval (`n * 7` days).

- **For monthly events:**
  - Verify that they appear on expected days.
  - If a scheduled date doesn’t exist, confirm behavior:
    - **If `use_last_day` = True**, it moves to the last valid day.
    - **If `use_last_day` = False**, it does not appear for that month.
  - Ensure event start weeks align with `test_results_df`.

✅ **Pass if:** Events follow correct recurrence rules.
❌ **Fail if:** Incorrect intervals or missing occurrences.

#### 2. Check the total number of events (using `test_results_df` and `existing_events_df`)
1. Compare event counts for each **Week Start Date** in `test_results_df` against `existing_events_df`.
2. Ensure no weeks have missing or extra occurrences.

✅ **Pass if:** Weekly event counts match expectations.
❌ **Fail if:** There are discrepancies in the event count.

---

## 3. Save Test Logs as CSV Files
Since this test runs in a Jupyter Notebook with Pandas, save structured results.

### Steps
1. **Store results in CSV files:**
   ```python
   import pandas as pd
   from datetime import datetime

   timestamp = datetime.now().strftime("%m%d%Y-%H%M%S")
   test_results_df.to_csv(f"test_cases_{timestamp}.csv", index=False)
   test_cases_data_df.to_csv(f"test_case_parameters_{timestamp}.csv", index=False)
   existing_events_df.to_csv(f"existing_events_{timestamp}.csv", index=False)
   ```

✅ **Pass if:** CSV files contain structured test results.
❌ **Fail if:** Data is missing or incorrectly formatted.

---

## Summary
- **Verify event occurrences** (`occurs_on`) → Use `existing_events_df`.
- **Count weekly event occurrences** (`count_weekly_events`) → Use `test_results_df`.
- **Compare expected vs. actual recurrence** → Use `test_cases_data_df` & `test_results_df`.
- **Ensure correct total event counts** → Compare `test_results_df` and `existing_events_df`.
- **These three DataFrames (`existing_events_df`, `test_cases_data_df`, `test_results_df`) are provided for running the test.**
- **Store results as CSV files** to keep a record of test accuracy.

✅ **Pass if:** Event dates, recurrence, and weekly counts match expected values.
❌ **Fail if:** Discrepancies exist in occurrences or event counts.
