
"""maintenance.py - Maintenance & Fault Management module"""

import ast
import os
from datetime import datetime
from equipment import equipment_list

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAINTENANCE_FILE = os.path.join(BASE_DIR, "Data", "maintenance.txt")

STATUSES = ["Pending", "In Progress", "Completed"]


def load_records():

    try:
        with open(MAINTENANCE_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip()

        if data == "":
            return []

        records = ast.literal_eval(data)

        if isinstance(records, list):
            return records

        return []

    except (FileNotFoundError, ValueError, SyntaxError):
        return []


def save_records(records):

    os.makedirs(os.path.dirname(MAINTENANCE_FILE), exist_ok=True)

    with open(MAINTENANCE_FILE, "w", encoding="utf-8") as f:
        f.write(repr(records))


def equipment_exists(equipment_id):

    for item in equipment_list:

        if item["equipment_id"].upper() == equipment_id.upper():
            return True

    return False


def clean_status(status):

    text = str(status).strip().lower()

    for valid in STATUSES:

        if text and valid.lower().startswith(text):
            return valid

    return None


def add_record(equipment_id, problem, reported_date="", status="Pending", remarks=""):

    equipment_id = str(equipment_id).strip().upper()
    problem = str(problem).strip()

    if not equipment_id or not problem:
        return False, "Equipment ID and problem cannot be empty.", None

    if not equipment_exists(equipment_id):
        return False, "Equipment ID '{}' was not found.".format(equipment_id), None

    reported_date = str(reported_date).strip() or datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(reported_date, "%Y-%m-%d")

    except ValueError:
        return False, "Invalid date. Use YYYY-MM-DD.", None

    status = clean_status(status)

    if status is None:
        return False, "Invalid status. Use: " + ", ".join(STATUSES) + ".", None

    records = load_records()

    last = max([int(r["maintenance_id"][1:]) for r in records] or [0])

    record = {
        "maintenance_id": "M{:03d}".format(last + 1),
        "equipment_id": equipment_id,
        "problem": problem,
        "reported_date": reported_date,
        "status": status,
        "remarks": str(remarks).strip()
    }

    records.append(record)
    save_records(records)

    return True, "Record {} added.".format(record["maintenance_id"]), record


def get_all_records():

    return load_records()


def find_record(maintenance_id):

    for r in load_records():

        if r["maintenance_id"].upper() == str(maintenance_id).strip().upper():
            return r

    return None


def update_record(maintenance_id, new_status=None, new_remarks=None):

    if new_status is not None and clean_status(new_status) is None:
        return False, "Invalid status. Use: " + ", ".join(STATUSES) + "."

    records = load_records()

    for r in records:

        if r["maintenance_id"].upper() == str(maintenance_id).strip().upper():

            if new_status is not None:
                r["status"] = clean_status(new_status)

            if new_remarks is not None:
                r["remarks"] = str(new_remarks).strip()

            save_records(records)

            return True, "Record {} updated.".format(r["maintenance_id"])

    return False, "Maintenance ID '{}' was not found.".format(maintenance_id)


def get_pending_records():

    return [
        r for r in load_records()
        if r["status"] in ("Pending", "In Progress")
    ]


def display_records(records):

    if not records:
        print("No records to show.")
        return

    print("{:<6} {:<10} {:<28} {:<11} {:<11}".format(
        "ID", "Equipment", "Problem", "Date", "Status"
    ))

    for r in records:

        print("{:<6} {:<10} {:<28} {:<11} {:<11}".format(
            r["maintenance_id"],
            r["equipment_id"],
            r["problem"][:27],
            r["reported_date"],
            r["status"]
        ))

        if r["remarks"]:
            print("       Remarks: " + r["remarks"])


def run_menu():

    while True:

        print("\n===== MAINTENANCE MANAGEMENT =====")
        print("1. Add Record")
        print("2. View All Records")
        print("3. Update Record")
        print("4. View Pending Records")
        print("5. Exit")

        choice = input("Choose (1-5): ").strip()

        if choice == "1":

            result = add_record(
                input("Equipment ID: "),
                input("Problem: "),
                input("Date (YYYY-MM-DD, Enter = today): "),
                input("Status (Enter = Pending): ") or "Pending",
                input("Remarks (optional): ")
            )

            print(result[1])

        elif choice == "2":

            display_records(get_all_records())

        elif choice == "3":

            mid = input("Maintenance ID (e.g. M001): ")
            status = input("New status (Enter = keep): ").strip() or None
            remarks = input("New remarks (Enter = keep): ").strip() or None

            print(update_record(mid, status, remarks)[1])

        elif choice == "4":

            display_records(get_pending_records())

        elif choice == "5":

            break

        else:

            print("Invalid choice.")


if __name__ == "__main__":
    run_menu()
