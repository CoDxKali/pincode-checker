import csv

def get_pincode_location(pincode):

    with open("data/pincode_data.csv", newline='', encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            if row["pincode"] == str(pincode):
                return float(row["latitude"]), float(row["longitude"])

    return None