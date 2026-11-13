# Test cases

Run commands from the project folder. By default, the program reads `hotel_sales.csv` beside the Python file. It also accepts an optional CSV filename, which makes it possible to try the assignment's missing `sales_old.csv` case.

## Test 1 — Normal input

Use the project's `hotel_sales.csv`, choose menu option `1`.

Expected daily revenue:

- 2026-10-01: Rs. 37,500
- 2026-10-02: Rs. 45,000
- 2026-10-03: Rs. 30,000
- Total: Rs. 1,12,500
- Best day: 2026-10-02 (Rs. 45,000)

Choose option `2` for room type totals: Standard Rs. 60,000 (53.33%) and Deluxe Rs. 52,500 (46.67%). Choose option `3` to capture the charts.

## Test 2 — Minimum input

Run `python hotel_revenue_analyzer.py testcases/test2_minimum_input.csv`, then choose option `1`.

Expected: one valid record; 2026-10-01 = Rs. 2,000; total = Rs. 2,000; best day = 2026-10-01 (Rs. 2,000).

## Test 3a — Invalid row

Run `python hotel_revenue_analyzer.py testcases/test3a_invalid_row.csv`, then choose option `1`.

Expected: warning for CSV row 8 because RoomsSold is negative; 6 valid records; skipped count 1; all valid totals match Test 1.

## Test 3b — Missing file

Run `python hotel_revenue_analyzer.py sales_old.csv`.

Expected: `Error: File 'sales_old.csv' not found...` and a helpful instruction.

## Test 4 — Room type scenario

Restore the sample `hotel_sales.csv`, choose menu option `2`.

Expected: Standard = Rs. 60,000 (53.33%); Deluxe = Rs. 52,500 (46.67%); total = Rs. 1,12,500.

## Screenshot checklist

Capture readable screenshots showing (1) Test 1 daily output and valid-record count, (2) Test 1 room-type output, (3) both charts, (4) Test 2 output, (5) Test 3a warning and totals, (6) Test 3b missing-file error. Save them in this `testcases` folder before submission. Do not include screenshots claiming a run you did not perform.
