
"""
CalibraLab - Calibration Management
BTech FY Project

Stores calibration records in a normal text file.

Fields:
equipment_id
last_calibration_date
next_due_date
status
remarks

Date format: YYYY-MM-DD
"""

import csv
from datetime import date
from pathlib import Path


# Text file location
DATA_FILE = Path(__file__).parent / "data" / "calibration.txt"

# Fields stored in the text file
FIELDS = [
    "equipment_id",
    "last_calibration_date",
    "next_due_date",
    "status",
    "remarks"
]


# Validate date format
def _parse_date(date_text):

    try:
        parsed = date.fromisoformat(date_text)

    except (TypeError, ValueError):
        raise ValueError("Enter date in YYYY-MM-DD format.")

    if parsed.isoformat() != date_text:
        raise ValueError("Use date format YYYY-MM-DD.")

    return parsed


# Calculate calibration status
def get_calibration_status(next_due_date, due_soon_days=None, today=None):

    due_date = _parse_date(next_due_date)

    current_date = today or date.today()

    days_remaining = (due_date - current_date).days

    if days_remaining < 0:
        return "Overdue"

    if due_soon_days is not None:

        if due_soon_days < 0:
            raise ValueError("Due soon days cannot be negative.")

        if days_remaining <= due_soon_days:
            return "Due Soon"

    return "Up to Date"


# Load records from text file
def load_records(file_path=DATA_FILE):

    path = Path(file_path)

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        return []

    records = []

    with path.open("r", encoding="utf-8", newline="") as file:

        reader = csv.DictReader(file, delimiter="|")

        if reader.fieldnames != FIELDS:
            if not reader.fieldnames:
                return []

            raise ValueError("Calibration text file has an invalid format.")

        for row in reader:

            record = {}

            for field in FIELDS:
                record[field] = row[field]

            records.append(record)

    return records


# Save records in text file
def save_records(records, file_path=DATA_FILE):

    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
            delimiter="|"
        )

        writer.writeheader()

        writer.writerows(records)


# Add a new calibration record
def add_record(records, equipment_id, last_calibration_date,
               next_due_date, remarks="", valid_equipment_ids=None,
               due_soon_days=None, today=None):

    equipment_id = str(equipment_id).strip()

    if not equipment_id:
        raise ValueError("Equipment ID cannot be empty.")

    if valid_equipment_ids is not None:

        if equipment_id not in valid_equipment_ids:
            raise ValueError("Unknown equipment ID: " + equipment_id)

    for item in records:

        if item["equipment_id"] == equipment_id:
            raise ValueError(
                "Calibration record already exists. Use update_record()."
            )

    _parse_date(last_calibration_date)
    _parse_date(next_due_date)

    record = {
        "equipment_id": equipment_id,
        "last_calibration_date": last_calibration_date,
        "next_due_date": next_due_date,
        "status": get_calibration_status(
            next_due_date, due_soon_days, today
        ),
        "remarks": str(remarks).strip()
    }

    records.append(record)

    return records


# View all calibration records
def view_records(records):

    return records


# Update an existing calibration record
def update_record(records, equipment_id,
                  last_calibration_date=None,
                  next_due_date=None,
                  remarks=None,
                  valid_equipment_ids=None,
                  due_soon_days=None,
                  today=None):

    equipment_id = str(equipment_id).strip()

    if valid_equipment_ids is not None:

        if equipment_id not in valid_equipment_ids:
            raise ValueError("Unknown equipment ID: " + equipment_id)

    for record in records:

        if record["equipment_id"] == equipment_id:

            new_last_date = (
                last_calibration_date
                if last_calibration_date is not None
                else record["last_calibration_date"]
            )

            new_due_date = (
                next_due_date
                if next_due_date is not None
                else record["next_due_date"]
            )

            _parse_date(new_last_date)
            _parse_date(new_due_date)

            record["last_calibration_date"] = new_last_date
            record["next_due_date"] = new_due_date

            if remarks is not None:
                record["remarks"] = str(remarks).strip()

            record["status"] = get_calibration_status(
                new_due_date, due_soon_days, today
            )

            return record

    raise ValueError(
        "No calibration record found for equipment ID: " + equipment_id
    )


# Refresh all calibration statuses
def refresh_statuses(records, due_soon_days=None, today=None):

    for record in records:

        record["status"] = get_calibration_status(
            record["next_due_date"], due_soon_days, today
        )

    return records


# Filter calibration records
def filter_records(records, status=None,
                   due_soon_days=None, today=None):

    valid_statuses = (
        "Up to Date",
        "Due Soon",
        "Overdue"
    )

    if status is not None and status not in valid_statuses:
        raise ValueError(
            "Status must be Up to Date, Due Soon, or Overdue."
        )

    matching = []

    for record in records:

        current_status = get_calibration_status(
            record["next_due_date"], due_soon_days, today
        )

        if status is None:

            if current_status in ("Due Soon", "Overdue"):
                matching.append(record)

        elif current_status == status:

            matching.append(record)

    return matching
