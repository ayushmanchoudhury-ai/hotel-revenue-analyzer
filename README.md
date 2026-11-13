# Hotel Revenue Analyzer

A small first-semester Python project that reads hotel sales from a CSV file, validates each row, calculates revenue, and displays summaries and charts.

## What the program does

- Reads `hotel_sales.csv` with Pandas.
- Calculates `Revenue = RoomsSold × Rate` for each valid row.
- Skips invalid data rows and explains why each row was skipped.
- Reports valid-record and skipped-row counts.
- Shows daily revenue, total revenue, and the best day.
- Shows revenue totals and percentage shares by room type.
- Draws a daily revenue chart and a room type revenue chart.
- Handles missing files, empty data, and invalid menu choices with helpful messages.

## Files

```text
hotel-revenue-analyzer/
├── hotel_revenue_analyzer.py
├── hotel_sales.csv
├── requirements.txt
├── README.md
└── testcases/
    ├── README.md
    ├── test2_minimum_input.csv
    └── test3a_invalid_row.csv
```

## Run in GitHub Codespaces

Open this repository in Codespaces, then in the terminal run:

```bash
python -m pip install -r requirements.txt
python hotel_revenue_analyzer.py
```

If your environment uses `python3`, replace `python` with `python3`.

The included CSV should produce these values:

```text
2026-10-01 : Rs. 37,500
2026-10-02 : Rs. 45,000
2026-10-03 : Rs. 30,000
Total revenue: Rs. 1,12,500
Best day: 2026-10-02 (Rs. 45,000)
```

## How the calculation works

For the first Standard row, 10 rooms were sold at Rs. 2,000 each:

```text
Revenue = RoomsSold × Rate
Revenue = 10 × 2,000 = Rs. 20,000
```

The program adds revenue from all rows that have the same date. On 2026-10-01, Standard revenue is Rs. 20,000 and Deluxe revenue is 5 × Rs. 3,500 = Rs. 17,500. Daily revenue is therefore Rs. 37,500. The best day is the date with the largest daily total.

For room-type share, the program divides that room type's revenue by total revenue and multiplies by 100. For Standard: 60,000 ÷ 112,500 × 100 = 53.33%.

## Data rules

- The CSV header must contain `Date`, `RoomType`, `RoomsSold`, and `Rate`.
- Dates must use `YYYY-MM-DD`; room type cannot be blank.
- RoomsSold and Rate must be finite numbers greater than or equal to zero.
- Empty, non-numeric, negative, infinite, or malformed values cause that record to be skipped with a row warning.
- Zero is accepted because the assignment says to skip negative values.
- If total revenue is zero, room-type shares are displayed as 0.00% to avoid division by zero.

## Test cases and screenshots

See [`testcases/README.md`](testcases/README.md) for all four assignment cases, their expected outputs, and a screenshot checklist. Run those cases yourself in Codespaces and save genuine screenshots in `testcases/` before submitting.

## GitHub submission overview

1. Sign in to GitHub and create a new repository, for example `hotel-revenue-analyzer`.
2. Upload these project files or open a Codespace and add them there.
3. In Codespaces, install dependencies and run the commands above.
4. Run each test case and save screenshots in `testcases/`.
5. Commit and push the finished files to your repository.
6. Share the repository link requested by your instructor.

## Presentation / viva prep

Suggested 5-part presentation: (1) problem and input CSV, (2) validation rules, (3) row revenue formula, (4) Pandas grouping for daily and room-type totals, (5) test results and charts.

Practice explaining these questions in your own words:

1. What is a CSV file, and why does this program use Pandas to read it?
2. How does one row become a revenue value?
3. Why are rows with invalid numbers skipped?
4. How are daily totals grouped and how is the best day selected?
5. How is a room type's percentage share calculated?
6. What happens if the CSV file is missing or has no valid rows?
7. What does `groupby("Date")` mean in this program?
8. Which line would you change to add another menu option?

Be ready to dry-run one record on paper: read its RoomsSold and Rate, multiply them, add its revenue to the matching date total, then compare daily totals to identify the best day.

## Limitations

This is a classroom console program, not hotel accounting software. It expects a simple comma-separated file with the required headers. It does not use a database or support multiple currencies. Always run the provided test cases before submission and explain the code yourself during the viva.
