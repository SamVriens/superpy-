import argparse
import csv
import os
from datetime import date, timedelta

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.

BOUGHT_CSV_FILE = "bought.csv"
SOLD_CSV_FILE = "sold.csv"
CURRENT_DAY_FILE = "current_day.txt"


# Function to create a CSV file if it doesn't exist
def create_csv_file(filename, header):
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)


# Function to create the "bought.csv" file
def create_bought_csv_file():
    create_csv_file(BOUGHT_CSV_FILE, ['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date'])


# Function to create the "sold.csv" file
def create_sold_csv_file():
    create_csv_file(SOLD_CSV_FILE, ['id', 'product_name', 'bought_id', 'sell_date', 'sell_price'])


# Function to load the bought data from the "bought.csv" file into a dictionary
def load_bought_data():
    bought_data = {}
    with open(BOUGHT_CSV_FILE, "r", newline="") as bought:
        reader = csv.DictReader(bought)
        for row in reader:
            bought_data[row["product_name"]] = row
    return bought_data


# This function retrieves the current day from an existing file named "current_day.txt" or creates the file with today's date if it doesn't exist.
def get_current_day():
    if os.path.isfile(CURRENT_DAY_FILE):
        with open(CURRENT_DAY_FILE, "r") as file:
            return file.read().strip()
    else:
        with open(CURRENT_DAY_FILE, "w") as file:
            current_day = date.today().isoformat()
            file.write(current_day)
            return current_day


# Function to set the current day in the "current_day.txt" file
def set_current_day(day):
    with open(CURRENT_DAY_FILE, "w") as file:
        file.write(day)


# Function to advance the current day by the specified number of days
def advance_time(days):
    current_day = get_current_day()
    current_date = date.fromisoformat(current_day)
    new_date = current_date + timedelta(days=days)
    new_day = new_date.isoformat()
    set_current_day(new_day)


# Function to report the inventory for the specified day
def report_inventory(now, yesterday):
    report_day = None
    if now:
        report_day = get_current_day()
    elif yesterday:
        current_day = get_current_day()
        current_date = date.fromisoformat(current_day)
        previous_date = current_date - timedelta(days=1)
        report_day = previous_date.isoformat()
    else:
        return

    with open(BOUGHT_CSV_FILE, "r", newline="") as bought_file:
        reader = csv.DictReader(bought_file)
        rows = [row for row in reader if row["buy_date"] == report_day]

    if rows:
        print("+--------------+-------+-----------+-----------------+")
        print("| Product Name | Count | Buy Price | Expiration Date |")
        print("+==============+=======+===========+=================+")
        for row in rows:
            print(
                f"| {row['product_name'].ljust(12)} "
                f"| {row['id'].ljust(5)} "
                f"| {row['buy_price'].ljust(9)} "
                f"| {row['expiration_date'].ljust(16)} |"
            )
        print("+--------------+-------+-----------+-----------------+")
    else:
        print("No inventory records for the specified day.")


# Main function to handle command-line arguments and execute appropriate actions
def main():
    parser = argparse.ArgumentParser(description="Welcome to the inventory system")
    parser.add_argument(
        "option",
        type=str,
        nargs="*",
        help="Options: buy, sell, report, report-revenue-profit",
    )

    parser.add_argument(
        "-p",
        "--product-name",
        type=str,
        
        dest="product",
        help="Name of the product",
    )
    parser.add_argument(
        "-d", "--buy-date", type=str, dest="date", help="Date when bought"
    )
    parser.add_argument(
        "--price", type=float, dest="price", help="Buying price of the product"
    )
    parser.add_argument(
        "-e",
        "--expiration-date",
        type=str,
        dest="expiration",
        help="Expiration date of the product",
    )
    parser.add_argument(
        "-s", "--sell_date", type=str, dest="sell_date", help="Date of selling"
    )
    parser.add_argument(
        "--sell-price", type=str, dest="sell_price", help="Selling price of the product"
    )
    parser.add_argument(
        "--advance-time",
        type=int,
        dest="advance_time",
        help="Advance the current day by the specified number of days",
    )
    parser.add_argument(
        "--now",
        action="store_true",
        dest="now",
        help="Report inventory for the current day",
    )
    parser.add_argument(
        "--yesterday",
        action="store_true",
        dest="yesterday",
        help="Report inventory for the previous day",
    )
    parser.add_argument(
        "--start-date", type=str, dest="start_date", help="Start date for revenue and profit reporting"
    )
    parser.add_argument(
        "--end-date", type=str, dest="end_date", help="End date for revenue and profit reporting"
    )

    parsed_args = parser.parse_args()

    create_bought_csv_file()
    create_sold_csv_file()
    bought_data = load_bought_data()

    if parsed_args.advance_time:
        advance_time(parsed_args.advance_time)

    if parsed_args.option and parsed_args.option[0] == "help":
        with open("usage_guide.txt", "r") as usage_guide:
            print(usage_guide.read())
        return    

    if parsed_args.option[0] == "buy":
        next_id = str(len(bought_data) + 1)
        with open(BOUGHT_CSV_FILE, "a", newline="") as bought:
            writer = csv.writer(bought)
            writer.writerow(
                [
                    next_id,
                    parsed_args.product,
                    parsed_args.date,
                    parsed_args.price,
                    parsed_args.expiration,
                ]
            )
        print(
            f"Bought {parsed_args.product} on {parsed_args.date} for {parsed_args.price} with expiration date {parsed_args.expiration} added to inventory"
        )

    elif parsed_args.option[0] == "sell":
        product_name = parsed_args.product
        bought_row = bought_data.get(product_name)
        if bought_row:
            bought_id = bought_row["id"]
            with open(SOLD_CSV_FILE, "a", newline="") as sold:
                writer = csv.writer(sold)
                writer.writerow(
                    [
                        str(len(bought_data) + 1),
                        product_name,
                        bought_id,
                        parsed_args.sell_date,
                        parsed_args.sell_price,
                    ]
                )
            print(f"Sold {product_name} for {parsed_args.sell_price}")
        else:
            print(f"{product_name} is out of stock!")

    elif parsed_args.option[0] == "report":
        report_inventory(parsed_args.now, parsed_args.yesterday)

    elif parsed_args.option[0] == "report-revenue-profit":
        start_date = parsed_args.start_date
        end_date = parsed_args.end_date

        revenue = 0
        profit = 0

        with open(SOLD_CSV_FILE, "r", newline="") as sold_file:
            reader = csv.DictReader(sold_file)
            rows = [row for row in reader if start_date <= row["sell_date"] <= end_date]

        for row in rows:
            bought_row = bought_data.get(row["product_name"])
            if bought_row:
                buy_price = float(bought_row["buy_price"])
                sell_price = float(row["sell_price"])
                revenue += sell_price
                profit += sell_price - buy_price

        print(f"Revenue from {start_date} to {end_date}: {revenue}")
        print(f"Profit from {start_date} to {end_date}: {profit}")


if __name__ == "__main__":
    main()
