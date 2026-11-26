
# CALIBRALAB - EQUIPMENT MANAGEMENT

import ast
import os


# EQUIPMENT FILE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EQUIPMENT_FILE = os.path.join(BASE_DIR, "Data", "equipment.txt")


# INITIAL EQUIPMENT RECORDS

initial_equipment = [

    {
        "equipment_id": "PHY-001",
        "name": "Digital Multimeter",
        "category": "Electrical",
        "quantity": 2,
        "location": "Physics Lab",
        "condition": "Working"
    },

    {
        "equipment_id": "PHY-002",
        "name": "Analog Ammeter",
        "category": "Electrical",
        "quantity": 2,
        "location": "Physics Lab",
        "condition": "Working"
    },

    {
        "equipment_id": "PHY-003",
        "name": "Analog Voltmeter",
        "category": "Electrical",
        "quantity": 2,
        "location": "Physics Lab",
        "condition": "Working"
    },

    {
        "equipment_id": "PHY-004",
        "name": "Rheostat",
        "category": "Electrical",
        "quantity": 3,
        "location": "Physics Lab",
        "condition": "Working"
    },

    {
        "equipment_id": "PHY-005",
        "name": "Vernier Caliper",
        "category": "Measurement",
        "quantity": 3,
        "location": "Physics Lab",
        "condition": "Working"
    }

]


# LOAD EQUIPMENT DATA

def load_equipment():

    os.makedirs(os.path.dirname(EQUIPMENT_FILE), exist_ok=True)

    if os.path.exists(EQUIPMENT_FILE):

        try:
            with open(EQUIPMENT_FILE, "r") as file:
                return ast.literal_eval(file.read())

        except (ValueError, SyntaxError):
            return initial_equipment.copy()

    save_equipment(initial_equipment)

    return initial_equipment.copy()


# SAVE EQUIPMENT DATA

def save_equipment(records):

    os.makedirs(os.path.dirname(EQUIPMENT_FILE), exist_ok=True)

    with open(EQUIPMENT_FILE, "w") as file:
        file.write(repr(records))


# EQUIPMENT LIST

equipment_list = load_equipment()


# ADD NEW EQUIPMENT

def add_equipment(equipment_id=None, name=None, category=None,
                  quantity=None, location=None, condition=None):

    if equipment_id is None:

        print("\n===== ADD NEW EQUIPMENT =====")

        equipment_id = input("Enter Equipment ID: ").strip()
        name = input("Enter Equipment Name: ").strip()
        category = input("Enter Category: ").strip()

        try:
            quantity = int(input("Enter Quantity: "))
        except ValueError:
            print("Please enter a valid quantity!")
            return False, "Invalid quantity!"

        location = input("Enter Lab Location: ").strip()
        condition = input("Enter Condition: ").strip()

    for item in equipment_list:

        if item["equipment_id"].upper() == equipment_id.upper():
            return False, "Equipment ID already exists!"

    if not all([equipment_id, name, category, location, condition]):
        return False, "All fields are required!"

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return False, "Please enter a valid quantity!"

    if quantity < 1:
        return False, "Quantity must be greater than zero!"

    equipment = {
        "equipment_id": equipment_id,
        "name": name,
        "category": category,
        "quantity": quantity,
        "location": location,
        "condition": condition
    }

    equipment_list.append(equipment)

    save_equipment(equipment_list)

    return True, "Equipment added successfully!"


# DISPLAY EQUIPMENT

def display_equipment():

    print("\n===== CALIBRALAB INVENTORY =====")

    for item in equipment_list:

        print("\nID:", item["equipment_id"])
        print("Name:", item["name"])
        print("Category:", item["category"])
        print("Quantity:", item["quantity"])
        print("Location:", item["location"])
        print("Condition:", item["condition"])

        print("------------------------------")


# SEARCH EQUIPMENT

def search_equipment(search_text=None):

    if search_text is None:
        search_text = input("Enter Equipment ID or Name: ").strip()

    results = []

    for item in equipment_list:

        if (search_text.lower() == item["equipment_id"].lower()
                or search_text.lower() == item["name"].lower()):

            results.append(item)

    return results


# UPDATE EQUIPMENT DETAILS

def update_equipment(equipment_id=None, field=None, value=None):

    if equipment_id is None:

        print("\n===== UPDATE EQUIPMENT =====")
        equipment_id = input("Enter Equipment ID: ").strip()

        for item in equipment_list:

            if equipment_id.lower() == item["equipment_id"].lower():

                print("\nEquipment Found!")
                print("1. Update Name")
                print("2. Update Category")
                print("3. Update Quantity")
                print("4. Update Location")
                print("5. Update Condition")

                choice = input("Enter your choice: ")

                fields = {
                    "1": "name",
                    "2": "category",
                    "3": "quantity",
                    "4": "location",
                    "5": "condition"
                }

                if choice not in fields:
                    print("Invalid Choice!")
                    return

                field = fields[choice]

                if field == "quantity":

                    try:
                        value = int(input("Enter New Quantity: "))
                    except ValueError:
                        print("Invalid quantity!")
                        return

                else:
                    value = input("Enter New Value: ").strip()

                success, message = update_equipment(
                    equipment_id, field, value
                )

                print(message)
                return

        print("Equipment Not Found!")
        return

    allowed_fields = [
        "name", "category", "quantity", "location", "condition"
    ]

    if field not in allowed_fields:
        return False, "Invalid field!"

    for item in equipment_list:

        if equipment_id.lower() == item["equipment_id"].lower():

            if field == "quantity":

                try:
                    value = int(value)
                except (ValueError, TypeError):
                    return False, "Please enter a valid quantity!"

                if value < 1:
                    return False, "Quantity must be greater than zero!"

            elif not value:
                return False, "Value cannot be empty!"

            item[field] = value

            save_equipment(equipment_list)

            return True, "Equipment updated successfully!"

    return False, "Equipment not found!"


# DELETE EQUIPMENT

def delete_equipment(equipment_id=None):

    if equipment_id is None:

        print("\n===== DELETE EQUIPMENT =====")
        equipment_id = input("Enter Equipment ID to delete: ").strip()

    for item in equipment_list:

        if equipment_id.lower() == item["equipment_id"].lower():

            equipment_list.remove(item)

            save_equipment(equipment_list)

            return True, "Equipment deleted successfully!"

    return False, "Equipment not found!"


# INVENTORY SUMMARY REPORT

def inventory_report():

    print("\n===== INVENTORY SUMMARY REPORT =====")

    total_equipment = len(equipment_list)
    total_quantity = 0

    for item in equipment_list:
        total_quantity = total_quantity + item["quantity"]

    print("Total Equipment Types:", total_equipment)
    print("Total Equipment Quantity:", total_quantity)

    print("\n===== EQUIPMENT DETAILS =====")

    for item in equipment_list:
        print(item["name"], "-", item["quantity"])


# EQUIPMENT CONDITION REPORT

def condition_report():

    print("\n===== EQUIPMENT CONDITION REPORT =====")

    working = 0
    attention = 0

    for item in equipment_list:

        if item["condition"] == "Working":
            working = working + 1
        else:
            attention = attention + 1

    print("Total Equipment Types:", len(equipment_list))
    print("Working Equipment:", working)
    print("Needs Attention:", attention)

    print("\n===== REPORT COMPLETED =====")


# SEARCH EQUIPMENT BY CATEGORY

def search_category(category_name=None):

    if category_name is None:
        category_name = input("Enter Category: ").strip()

    results = []

    for item in equipment_list:

        if category_name.lower() == item["category"].lower():
            results.append(item)

    return results


# MAIN MENU

if __name__ == "__main__":

    while True:

        print("\n===== CALIBRALAB =====")
        print("1. Display Equipment")
        print("2. Add Equipment")
        print("3. Search Equipment")
        print("4. Update Equipment")
        print("5. Delete Equipment")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_equipment()

        elif choice == "2":
            result = add_equipment()
            print(result[1])

        elif choice == "3":
            results = search_equipment()

            if results:
                print("Equipment Found:", results)
            else:
                print("No equipment found!")

        elif choice == "4":
            update_equipment()

        elif choice == "5":
            result = delete_equipment()
            print(result[1])

        elif choice == "6":
            print("Thank you for using CalibraLab!")
            break

        else:
            print("Invalid Choice!")
