
from flask import Flask, render_template
from equipment import equipment_list

app = Flask(__name__)


@app.route("/")
def home():

    total_equipment = len(equipment_list)

    total_units = 0
    for item in equipment_list:
        total_units = total_units + item["quantity"]

    working_equipment = 0
    under_maintenance = 0

    for item in equipment_list:

        if item["condition"] == "Working":
            working_equipment = working_equipment + 1

        else:
            under_maintenance = under_maintenance + 1

    return render_template(
        "index.html",
        equipment=equipment_list,
        total_equipment=total_equipment,
        total_units=total_units,
        working_equipment=working_equipment,
        under_maintenance=under_maintenance
    )


if __name__ == "__main__":
    app.run(debug=True)
