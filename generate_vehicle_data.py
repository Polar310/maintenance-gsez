import csv

csv_file = "Vehicle_and_Equipment_Registry - Vehicle_and_Equipment_Registry.csv.csv"
vehicle_info = {}

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["Vehicle/equipment_NO"].strip()
        # Remove the key from the row to avoid duplication
        vehicle_info[key] = {
            "Asset": row["Asset"].strip(),
            "Make": row["Make"].strip(),
            "Vehicle/equipment_NO": key,
            "Application": row["Application"].strip(),
            "Depart": row["Depart"].strip(),
            "Entity": row["Entity"].strip(),
            "Location": row["Location"].strip()
        }

# If you want to write this to vehicle_data.py:
with open("vehicle_data.py", "w", encoding="utf-8") as f:
    f.write("#store all vehicle info\n")
    f.write("vehicle_info = ")
    f.write(repr(vehicle_info))
    f.write("\n")