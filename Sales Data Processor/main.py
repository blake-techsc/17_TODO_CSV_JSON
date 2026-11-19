import csv
from pathlib import Path

folder = Path(__file__).parent

def read_sales(filename):
    """Reads (row_number, row_dict) for each record in the CSV, header skipped."""
    with open(filename, newline="") as csv_file:
        for number, row in enumerate(csv.DictReader(csv_file), start=1):
            yield number, row

def validate_sale(row):
    """Return (qty, price) for a valid record, or an error-message string if invalid."""
    if not (row.get("Customer") or "").strip() or not (row.get("Item") or "").strip():
        return "Blank Customer or Item"

    try:
        qty = int(str(row.get("Qty")).strip())
        if qty <= 0:
            return "Value must be positive: " + str(row.get("Qty"))
        price = float(str(row.get("Price Total")).strip())
        if price < 0:
            return "Negative price: " + str(row.get("Price Total"))
    except (TypeError, ValueError):
        return "Invalid Qty or Price Total: " + str(row.get("Qty"))

    return qty, price

def update_summary(summary, item, qty, price):
    """Add one valid sale's quantity and revenue to the running item totals."""
    totals = summary.setdefault(item, [0, 0.0])
    totals[0] += qty
    totals[1] += price

def log_error(log_file, row_number, reason, row):
    """Write one rejected record to the error log file."""
    log_file.write(f"Line {row_number} | {reason} | {','.join(filter(None, row.values()))}\n")

def save_summary(summary, filename):
    """Write grouped totals to the summary CSV, sorted alphabetically by item."""
    with open(filename, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Item", "Qty", "Price Total"])
        for item in sorted(summary):
            writer.writerow([item, summary[item][0], f"{summary[item][1]:.2f}"])

def display_totals(total_qty, subtotal, invalid):
    """Print final totals, invalid count, and output filenames."""
    print("Sales Processing Complete")
    print("-------------------------")
    print(f"Total Items Sold: {total_qty}")
    print(f"Sales Subtotal: ${subtotal:.2f}")
    print(f"Invalid Records: {invalid}")
    print("Files Created: sales_summary.csv, errors.log")

def main():
    """Read, validate, log, save, and report."""
    summary = {}
    total_qty = 0
    subtotal = 0.0
    invalid = 0

    try:
        with open(folder / "errors.log", "w") as log_file:
            for number, row in read_sales(folder / "sales.csv"):
                result = validate_sale(row)
                if isinstance(result, str):
                    log_error(log_file, number, result, row)
                    invalid += 1
                else:
                    qty, price = result
                    update_summary(summary, row["Item"].strip(), qty, price)
                    total_qty += qty
                    subtotal += price
    except FileNotFoundError:
        print("sales.csv not found, put it in the same folder as this script.")
        return

    save_summary(summary, folder / "sales_summary.csv")
    display_totals(total_qty, subtotal, invalid)

if __name__ == "__main__":
    main()