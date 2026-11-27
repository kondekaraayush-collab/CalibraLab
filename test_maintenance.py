
"""Automated checks for maintenance.py."""

import os
import tempfile
import maintenance

tmp = tempfile.mkdtemp()

maintenance.MAINTENANCE_FILE = os.path.join(tmp, "maintenance.txt")
maintenance.EQUIPMENT_FILE = os.path.join(tmp, "equipment.txt")

# Create sample equipment data
with open(maintenance.EQUIPMENT_FILE, "w") as f:
    f.write(repr([
        {"equipment_id": "EQ001"},
        {"equipment_id": "EQ002"}
    ]))

results = []


def check(name, condition):
    results.append((name, condition))
    print(("PASS  " if condition else "FAIL  ") + name)


# Missing file loads as empty list
check("Missing file loads as empty list",
      maintenance.load_records() == [])

# Add and view
ok, msg, rec = maintenance.add_record(
    "EQ001", "Display not working",
    "2026-11-02", "Pending", "Needs inspection"
)

check("Add record with all details",
      ok and rec["maintenance_id"] == "M001")

check("View record after adding",
      len(maintenance.get_all_records()) == 1)

# Multiple records
maintenance.add_record("EQ002", "Sensor drift")
maintenance.add_record(
    "eq001", "Power cable damaged",
    "2026-11-05", "in progress"
)

check("Add more than one record",
      len(maintenance.get_all_records()) == 3)

# Updates
ok, _ = maintenance.update_record("M001", "In Progress")

check("Pending -> In Progress",
      ok and maintenance.find_record("M001")["status"] == "In Progress")

ok, _ = maintenance.update_record("M001", "Completed", "Fixed")

check("In Progress -> Completed",
      ok and maintenance.find_record("M001")["status"] == "Completed")

# Pending filter
pending_ids = [
    r["maintenance_id"]
    for r in maintenance.get_pending_records()
]

check("Pending view shows Pending + In Progress",
      pending_ids == ["M002", "M003"])

# Data reload
check("Records reload from file",
      len(maintenance.load_records()) == 3)

# Error handling
ok, msg, _ = maintenance.add_record("EQ999", "Broken")

check("Unknown equipment ID gives clear message",
      (not ok) and "not found" in msg)

ok, _, _ = maintenance.add_record(
    "EQ001", "x", "02-11-2026"
)

check("Bad date rejected", not ok)

ok, _, _ = maintenance.add_record(
    "EQ001", "x", "2026-11-02", "Broken"
)

check("Bad status rejected", not ok)

ok, _ = maintenance.update_record("M999", "Completed")

check("Unknown maintenance ID handled", not ok)

# Empty text file
with open(maintenance.MAINTENANCE_FILE, "w") as f:
    f.write("")

check("Empty text file does not crash",
      maintenance.load_records() == [])

print("\n{}/{} checks passed".format(
    sum(c for _, c in results), len(results)
))
