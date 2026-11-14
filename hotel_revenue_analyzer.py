"""Beginner-friendly Hotel Revenue Analyzer (Python 3 + Pandas)."""

from pathlib import Path
import math
import sys

import pandas as pd


REQUIRED_COLUMNS = ["Date", "RoomType", "RoomsSold", "Rate"]
DATA_FILE = "hotel_sales.csv"


def format_rupees(amount):
    """Format a number using Indian digit grouping, for example 112500 -> 1,12,500."""
    rounded_amount = round(float(amount), 2)
    whole_part = int(rounded_amount)
    decimal_part = abs(rounded_amount - whole_part)

    last_three_digits = str(abs(whole_part) % 1000).zfill(3)
    remaining_digits = str(abs(whole_part) // 1000)
    grouped_parts = []

    while remaining_digits:
        grouped_parts.insert(0, remaining_digits[-2:])
        remaining_digits = remaining_digits[:-2]

    if grouped_parts:
        whole_text = ",".join(grouped_parts + [last_three_digits])
    else:
        whole_text = last_three_digits.lstrip("0") or "0"

    if whole_part < 0:
        whole_text = "-" + whole_text
    if decimal_part:
        return f"Rs. {whole_text}.{round(decimal_part * 100):02d}"
    return f"Rs. {whole_text}"


def load_and_validate_data(file_path):
    """Read a CSV with Pandas, print row warnings, and return only valid records."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File '{path.name}' not found. Put it beside this program and try again.")

    try:
        data = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    except pd.errors.EmptyDataError as error:
        raise ValueError("The CSV file is empty. Add the required header and at least one data row.") from error
    except pd.errors.ParserError as error:
        raise ValueError("The CSV structure is invalid. Check that every row has exactly four comma-separated columns.") from error
    except UnicodeDecodeError as error:
        raise ValueError("The CSV encoding could not be read. Save it as UTF-8 and try again.") from error

    data.columns = [str(column).strip() for column in data.columns]
    if data.columns.duplicated().any():
        raise ValueError("The CSV has duplicate column names. Each required column must appear only once.")
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Missing required column(s): {missing_text}. Required columns: {', '.join(REQUIRED_COLUMNS)}")

    valid_records = []
    skipped_count = 0

    # DataFrame index starts at 0; CSV line 1 contains the header, so add 2.
    for index, row in data.iterrows():
        csv_row_number = index + 2
        date_text = str(row["Date"]).strip()
        room_type = str(row["RoomType"]).strip()
        rooms_text = str(row["RoomsSold"]).strip()
        rate_text = str(row["Rate"]).strip()

        problems = []
        parsed_date = pd.to_datetime(date_text, format="%Y-%m-%d", errors="coerce")
        if pd.isna(parsed_date):
            problems.append("Date must use YYYY-MM-DD format")
        if not room_type:
            problems.append("RoomType cannot be empty")

        try:
            rooms_sold = float(rooms_text)
            if not math.isfinite(rooms_sold):
                raise ValueError
            if rooms_sold < 0:
                problems.append("RoomsSold must be 0 or more")
        except ValueError:
            rooms_sold = None
            problems.append("RoomsSold must be a number")

        try:
            rate = float(rate_text)
            if not math.isfinite(rate):
                raise ValueError
            if rate < 0:
                problems.append("Rate must be 0 or more")
        except ValueError:
            rate = None
            problems.append("Rate must be a number")

        if problems:
            skipped_count += 1
            print(f"Warning: Row {csv_row_number} skipped - {'; '.join(problems)}.")
            continue

        valid_records.append(
            {
                "Date": parsed_date.strftime("%Y-%m-%d"),
                "RoomType": room_type,
                "RoomsSold": rooms_sold,
                "Rate": rate,
                "Revenue": rooms_sold * rate,
            }
        )

    clean_data = pd.DataFrame(valid_records, columns=REQUIRED_COLUMNS + ["Revenue"])
    print(f"Valid records analysed: {len(clean_data)}")
    if skipped_count:
        print(f"Rows skipped: {skipped_count}")
    return clean_data


def show_daily_revenue(data):
    """Print revenue for each date, total revenue, and the best revenue day."""
    if data.empty:
        print("No valid records to analyse.")
        return

    daily_totals = data.groupby("Date")["Revenue"].sum().sort_index()
    print("\nDAILY REVENUE")
    for date, revenue in daily_totals.items():
        print(f"{date} : {format_rupees(revenue)}")

    total_revenue = daily_totals.sum()
    best_day = daily_totals.idxmax()
    print(f"Total revenue: {format_rupees(total_revenue)}")
    print(f"Best day: {best_day} ({format_rupees(daily_totals[best_day])})")


def show_room_type_revenue(data):
    """Print revenue and percentage share for each room type."""
    if data.empty:
        print("No valid records to analyse.")
        return

    room_totals = data.groupby("RoomType")["Revenue"].sum().sort_index()
    total_revenue = room_totals.sum()
    print("\nREVENUE BY ROOM TYPE")
    for room_type, revenue in room_totals.items():
        share = (revenue / total_revenue * 100) if total_revenue else 0
        print(f"{room_type} : {format_rupees(revenue)} ({share:.2f}%)")
    print(f"Total revenue: {format_rupees(total_revenue)}")


def show_charts(data):
    """Display simple daily and room-type revenue charts with Matplotlib."""
    if data.empty:
        print("No valid records to chart.")
        return

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Charts need Matplotlib. Install it with: pip install matplotlib")
        return

    daily_totals = data.groupby("Date")["Revenue"].sum().sort_index()
    room_totals = data.groupby("RoomType")["Revenue"].sum().sort_index()

    figure, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].bar(daily_totals.index, daily_totals.values, color="steelblue")
    axes[0].set_title("Daily Hotel Revenue")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Revenue (Rs.)")
    axes[0].tick_params(axis="x", rotation=25)

    axes[1].bar(room_totals.index, room_totals.values, color="darkorange")
    axes[1].set_title("Revenue by Room Type")
    axes[1].set_xlabel("Room type")
    axes[1].set_ylabel("Revenue (Rs.)")

    figure.tight_layout()
    figure.savefig("testcases/hotel_revenue_charts.png")


def main():
    """Load the default CSV and run the menu until the user exits."""
    # An optional filename makes it easy to demonstrate the missing-file test.
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    else:
        file_path = Path(__file__).resolve().parent / DATA_FILE
    try:
        data = load_and_validate_data(file_path)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        return

    while True:
        print("\n=== HOTEL REVENUE ANALYZER ===")
        print("1. Daily revenue and best day")
        print("2. Revenue by room type")
        print("3. Show charts")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            show_daily_revenue(data)
        elif choice == "2":
            show_room_type_revenue(data)
        elif choice == "3":
            show_charts(data)
        elif choice == "4":
            print("Thank you for using Hotel Revenue Analyzer.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
