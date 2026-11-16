
# CALIBRALAB - EQUIPMENT MANAGEMENT

# Initial equipment records

equipment_list = [

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


# ADD NEW EQUIPMENT

def add_equipment():

    print("\n===== ADD NEW EQUIPMENT =====")

    equipment_id = input("Enter Equipment ID: ").strip()

    for item in equipment_list:

        if item["equipment_id"] == equipment_id:
            print("Equipment ID already exists!")
            return

    name = input("Enter Equipment Name: ").strip()
    category = input("Enter Category: ").strip()

    try:
        quantity = int(input("Enter Quantity: "))
    except ValueError:
        print("Please enter a valid quantity!")
        return

    if quantity < 1:
        print("Quantity must be greater than zero!")
        return

    location = input("Enter Lab Location: ").strip()
    condition = input("Enter Condition: ").strip()

    if not all([equipment_id, name, category,
                location, condition]):
        print("All fields are required!")
        return

    equipment = {
        "equipment_id": equipment_id,
        "name": name,
        "category": category,
        "quantity": quantity,
        "location": location,
        "condition": condition
    }

    equipment_list.append(equipment)

    print("\nEquipment added successfully!")


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

def search_equipment():

    print("\n===== SEARCH EQUIPMENT =====")

    search_text = input("Enter Equipment ID or Name: ")

    found = False

    for item in equipment_list:

        if search_text == item["equipment_id"] or search_text == item["name"]:

            print("\nEquipment Found!")
            print("ID:", item["equipment_id"])
            print("Name:", item["name"])
            print("Category:", item["category"])
            print("Quantity:", item["quantity"])
            print("Location:", item["location"])
            print("Condition:", item["condition"])

            found = True

    if found == False:
        print("No equipment found!")


# UPDATE EQUIPMENT DETAILS

def update_equipment():

    print("\n===== UPDATE EQUIPMENT =====")

    equipment_id = input("Enter Equipment ID: ")

    found = False

    for item in equipment_list:

        if equipment_id == item["equipment_id"]:

            found = True

            print("\nEquipment Found!")
            print("1. Update Name")
            print("2. Update Category")
            print("3. Update Quantity")
            print("4. Update Location")
            print("5. Update Condition")

            choice = input("Enter your choice: ")

            if choice == "1":

                new_name = input("Enter New Name: ")

                if new_name != "":
                    item["name"] = new_name
                    print("Name Updated Successfully!")
                else:
                    print("Name cannot be empty!")

            elif choice == "2":

                new_category = input("Enter New Category: ")

                if new_category != "":
                    item["category"] = new_category
                    print("Category Updated Successfully!")
                else:
                    print("Category cannot be empty!")

            elif choice == "3":

                try:
                    quantity = int(input("Enter New Quantity: "))

                    if quantity > 0:
                        item["quantity"] = quantity
                        print("Quantity Updated Successfully!")
                    else:
                        print("Quantity must be greater than zero!")

                except ValueError:
                    print("Please enter a valid quantity!")

            elif choice == "4":

                new_location = input("Enter New Location: ")

                if new_location != "":
                    item["location"] = new_location
                    print("Location Updated Successfully!")
                else:
                    print("Location cannot be empty!")

            elif choice == "5":

                new_condition = input("Enter New Condition: ")

                if new_condition != "":
                    item["condition"] = new_condition
                    print("Condition Updated Successfully!")
                else:
                    print("Condition cannot be empty!")

            else:
                print("Invalid Choice!")

            break

    if found == False:
        print("Equipment Not Found!")


# DELETE EQUIPMENT

def delete_equipment():

    print("\n===== DELETE EQUIPMENT =====")

    equipment_id = input("Enter Equipment ID to delete: ")

    found = False

    for item in equipment_list:

        if equipment_id == item["equipment_id"]:

            found = True

            print("\nEquipment Found!")
            print("Name:", item["name"])

            confirm = input("Do you want to delete this equipment? (yes/no): ")

            if confirm == "yes":
                equipment_list.remove(item)
                print("Equipment Deleted Successfully!")

            else:
                print("Deletion Cancelled!")

            break

    if found == False:
        print("Equipment Not Found!")


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

def search_category():

    print("\n===== SEARCH BY CATEGORY =====")

    category_name = input("Enter Category: ")

    found = False

    for item in equipment_list:

        if category_name == item["category"]:

            print("\nEquipment Found!")
            print("ID:", item["equipment_id"])
            print("Name:", item["name"])
            print("Category:", item["category"])
            print("Quantity:", item["quantity"])
            print("Location:", item["location"])
            print("Condition:", item["condition"])

            found = True

    if found == False:
        print("No equipment found in this category!")




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
            add_equipment()

        elif choice == "3":
            search_equipment()

        elif choice == "4":
            update_equipment()

        elif choice == "5":
            delete_equipment()

        elif choice == "6":
            print("Thank you for using CalibraLab!")
            break

        else:
            print("Invalid Choice!")