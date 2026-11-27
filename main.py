
from flask import Flask, render_template, request, redirect, url_for, flash, send_file

from equipment import (
    equipment_list,
    add_equipment,
    update_equipment,
    delete_equipment,
    search_equipment
)

from maintenance import (
    add_record,
    get_all_records,
    get_pending_records
)

from calibration import (
    load_records,
    save_records,
    add_record as add_calibration_record,
    update_record as update_calibration_record,
    refresh_statuses,
    filter_records
)

from pathlib import Path
from io import BytesIO
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from xml.sax.saxutils import escape


app = Flask(__name__)
app.secret_key = "calibralab_secret_key"

Path(__file__).parent.joinpath("data").mkdir(exist_ok=True)

DUE_SOON_DAYS = 10


def get_calibration_records():
    records = load_records()
    refresh_statuses(records, due_soon_days=DUE_SOON_DAYS)
    save_records(records)
    return records


# DASHBOARD

@app.route("/")
def home():

    total_equipment = len(equipment_list)

    total_units = 0
    working_equipment = 0
    under_maintenance = 0

    for item in equipment_list:
        total_units += int(item.get("quantity", 0))

        if item.get("condition") == "Working":
            working_equipment += 1
        else:
            under_maintenance += 1

    if total_equipment > 0:
        working_percentage = (working_equipment / total_equipment) * 100
        non_working_percentage = (under_maintenance / total_equipment) * 100
    else:
        working_percentage = 0
        non_working_percentage = 0

    maintenance_records = get_all_records()
    pending_records = get_pending_records()

    total_maintenance = len(maintenance_records)
    pending_maintenance = len(pending_records)

    search_text = request.args.get("search", "").strip()
    search_results = []

    if search_text:
        search_results = search_equipment(search_text)

    # CALIBRATION RECORDS

    all_calibration_records = get_calibration_records()

    selected_calibration_status = request.args.get(
        "calibration_status", "All"
    )

    if selected_calibration_status == "All":
        calibration_records = all_calibration_records
    else:
        calibration_records = filter_records(
            all_calibration_records,
            status=selected_calibration_status,
            due_soon_days=DUE_SOON_DAYS
        )

    total_calibration = len(all_calibration_records)

    due_soon_calibration = len(filter_records(
        all_calibration_records,
        status="Due Soon",
        due_soon_days=DUE_SOON_DAYS
    ))

    overdue_calibration = len(filter_records(
        all_calibration_records,
        status="Overdue",
        due_soon_days=DUE_SOON_DAYS
    ))

    return render_template(
        "index.html",

        # BOTH NAMES ARE PASSED FOR TEMPLATE COMPATIBILITY
        equipment_list=equipment_list,
        equipment=equipment_list,

        total_equipment=total_equipment,
        total_units=total_units,
        working_equipment=working_equipment,
        under_maintenance=under_maintenance,
        working_percentage=working_percentage,
        non_working_percentage=non_working_percentage,
        maintenance_records=maintenance_records,
        total_maintenance=total_maintenance,
        pending_maintenance=pending_maintenance,
        search_results=search_results,
        search_text=search_text,
        calibration_records=calibration_records,
        all_calibration_records=all_calibration_records,
        total_calibration=total_calibration,
        due_soon_calibration=due_soon_calibration,
        overdue_calibration=overdue_calibration,
        selected_calibration_status=selected_calibration_status,
        due_soon_days=DUE_SOON_DAYS
    )


# ADD EQUIPMENT

@app.route("/add_equipment", methods=["POST"])
def add_equipment_route():

    success, message = add_equipment(
        request.form.get("equipment_id", "").strip(),
        request.form.get("name", "").strip(),
        request.form.get("category", "").strip(),
        request.form.get("quantity", ""),
        request.form.get("location", "").strip(),
        request.form.get("condition", "").strip()
    )

    flash(message)
    return redirect(url_for("home"))


# UPDATE EQUIPMENT

@app.route("/update_equipment", methods=["POST"])
def update_equipment_route():

    success, message = update_equipment(
        request.form.get("equipment_id", "").strip(),
        request.form.get("field", "").strip(),
        request.form.get("value", "").strip()
    )

    flash(message)
    return redirect(url_for("home"))


# DELETE EQUIPMENT

@app.route("/delete_equipment", methods=["POST"])
def delete_equipment_route():

    success, message = delete_equipment(
        request.form.get("equipment_id", "").strip()
    )

    flash(message)
    return redirect(url_for("home"))


# ADD MAINTENANCE RECORD

@app.route("/add_maintenance", methods=["POST"])
def add_maintenance_route():

    equipment_id = request.form.get("equipment_id", "").strip()
    problem = request.form.get("problem", "").strip()
    reported_date = request.form.get("reported_date", "").strip()
    status = request.form.get("status", "Pending").strip()
    remarks = request.form.get("remarks", "").strip()

    success, message, record = add_record(
        equipment_id,
        problem,
        reported_date,
        status,
        remarks
    )

    flash(message)
    return redirect(url_for("home"))


# ADD CALIBRATION RECORD

@app.route("/add_calibration", methods=["POST"])
def add_calibration_route():

    equipment_id = request.form.get("equipment_id", "").strip()

    last_calibration_date = request.form.get(
        "last_calibration_date", ""
    ).strip()

    next_due_date = request.form.get("next_due_date", "").strip()
    remarks = request.form.get("remarks", "").strip()

    valid_equipment_ids = [
        item.get("equipment_id", "") for item in equipment_list
    ]

    try:
        calibration_records = load_records()

        add_calibration_record(
            calibration_records,
            equipment_id,
            last_calibration_date,
            next_due_date,
            remarks,
            valid_equipment_ids=valid_equipment_ids,
            due_soon_days=DUE_SOON_DAYS
        )

        save_records(calibration_records)
        flash("Calibration record added successfully.")

    except ValueError as error:
        flash(str(error))

    return redirect(url_for("home") + "#calibration")


# UPDATE CALIBRATION RECORD

@app.route("/update_calibration", methods=["POST"])
def update_calibration_route():

    equipment_id = request.form.get("equipment_id", "").strip()

    last_calibration_date = request.form.get(
        "last_calibration_date", ""
    ).strip()

    next_due_date = request.form.get("next_due_date", "").strip()
    remarks = request.form.get("remarks", "").strip()

    if last_calibration_date == "":
        last_calibration_date = None

    if next_due_date == "":
        next_due_date = None

    if remarks == "":
        remarks = None

    valid_equipment_ids = [
        item.get("equipment_id", "") for item in equipment_list
    ]

    try:
        calibration_records = load_records()

        update_calibration_record(
            calibration_records,
            equipment_id,
            last_calibration_date=last_calibration_date,
            next_due_date=next_due_date,
            remarks=remarks,
            valid_equipment_ids=valid_equipment_ids,
            due_soon_days=DUE_SOON_DAYS
        )

        save_records(calibration_records)
        flash("Calibration record updated successfully.")

    except ValueError as error:
        flash(str(error))

    return redirect(url_for("home") + "#calibration")


# DOWNLOAD EQUIPMENT PDF REPORT

@app.route("/equipment_report/<equipment_id>")
def equipment_report(equipment_id):

    selected_equipment = None

    for item in equipment_list:
        if str(item.get("equipment_id", "")).upper() == equipment_id.upper():
            selected_equipment = item
            break

    if selected_equipment is None:
        flash("Equipment not found.")
        return redirect(url_for("home"))

    all_records = get_all_records()

    equipment_records = [
        record for record in all_records
        if record.get("equipment_id", "").upper() == equipment_id.upper()
    ]

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("CalibraLab", styles["Title"]))
    content.append(Paragraph("Equipment Details Report", styles["Heading2"]))
    content.append(Spacer(1, 15))

    content.append(Paragraph(
        "Generated on: " + datetime.now().strftime("%d-%m-%Y %H:%M"),
        styles["Normal"]
    ))

    content.append(Spacer(1, 20))

    equipment_details = [
        ["Equipment ID", str(selected_equipment.get("equipment_id", "N/A"))],
        ["Equipment Name", str(selected_equipment.get("name", "N/A"))],
        ["Category", str(selected_equipment.get("category", "N/A"))],
        ["Quantity", str(selected_equipment.get("quantity", "N/A"))],
        ["Location", str(selected_equipment.get("location", "N/A"))],
        ["Condition", str(selected_equipment.get("condition", "N/A"))]
    ]

    details_table = Table(equipment_details, colWidths=[150, 300])

    details_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    content.append(details_table)
    content.append(Spacer(1, 25))

    content.append(Paragraph("Maintenance History", styles["Heading2"]))
    content.append(Spacer(1, 10))

    if equipment_records:
        maintenance_data = [
            ["Problem", "Date", "Status", "Remarks"]
        ]

        for record in equipment_records:
            maintenance_data.append([
                Paragraph(
                    escape(str(record.get("problem", ""))),
                    styles["Normal"]
                ),
                str(record.get("reported_date", "")),
                str(record.get("status", "")),
                Paragraph(
                    escape(str(record.get("remarks", ""))),
                    styles["Normal"]
                )
            ])

        maintenance_table = Table(
            maintenance_data,
            colWidths=[120, 85, 85, 120],
            repeatRows=1
        )

        maintenance_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))

        content.append(maintenance_table)

    else:
        content.append(Paragraph(
            "No maintenance records available for this equipment.",
            styles["Normal"]
        ))

    content.append(Spacer(1, 25))

    content.append(Paragraph(
        "CalibraLab - Laboratory Equipment Management System",
        styles["Italic"]
    ))

    document.build(content)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"CalibraLab_Equipment_{equipment_id}_Report.pdf",
        mimetype="application/pdf"
    )


# DOWNLOAD DATE-WISE PDF REPORT

@app.route("/period_report", methods=["POST"])
def period_report():

    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

    except ValueError:
        flash("Please select valid start and end dates.")
        return redirect(url_for("home") + "#reports")

    if start > end:
        flash("Start date cannot be after the end date.")
        return redirect(url_for("home") + "#reports")

    all_maintenance_records = get_all_records()
    all_calibration_records = get_calibration_records()

    period_maintenance_records = []

    for record in all_maintenance_records:
        try:
            record_date = datetime.strptime(
                record.get("reported_date", ""),
                "%Y-%m-%d"
            ).date()

            if start <= record_date <= end:
                period_maintenance_records.append(record)

        except ValueError:
            continue

    period_calibration_records = []

    for record in all_calibration_records:
        try:
            record_date = datetime.strptime(
                record.get("last_calibration_date", ""),
                "%Y-%m-%d"
            ).date()

            if start <= record_date <= end:
                period_calibration_records.append(record)

        except ValueError:
            continue

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("CalibraLab", styles["Title"]))
    content.append(Paragraph("Date-Wise Activity Report", styles["Heading2"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(
        "Selected Period: "
        + start.strftime("%d-%m-%Y")
        + " to "
        + end.strftime("%d-%m-%Y"),
        styles["Normal"]
    ))

    content.append(Paragraph(
        "Generated on: " + datetime.now().strftime("%d-%m-%Y %H:%M"),
        styles["Normal"]
    ))

    content.append(Spacer(1, 20))

    # MAINTENANCE REPORT

    content.append(Paragraph("Maintenance Records", styles["Heading2"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "Total maintenance records: "
        + str(len(period_maintenance_records)),
        styles["Normal"]
    ))

    content.append(Spacer(1, 8))

    if period_maintenance_records:

        maintenance_data = [
            ["Equipment ID", "Problem", "Date", "Status"]
        ]

        for record in period_maintenance_records:
            maintenance_data.append([
                str(record.get("equipment_id", "")),
                Paragraph(
                    escape(str(record.get("problem", ""))),
                    styles["Normal"]
                ),
                str(record.get("reported_date", "")),
                str(record.get("status", ""))
            ])

        maintenance_table = Table(
            maintenance_data,
            colWidths=[90, 190, 95, 100],
            repeatRows=1
        )

        maintenance_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))

        content.append(maintenance_table)

    else:
        content.append(Paragraph(
            "No maintenance records found in this period.",
            styles["Normal"]
        ))

    content.append(Spacer(1, 25))

    # CALIBRATION REPORT

    content.append(Paragraph("Calibration Records", styles["Heading2"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "Total calibration records: "
        + str(len(period_calibration_records)),
        styles["Normal"]
    ))

    content.append(Spacer(1, 8))

    if period_calibration_records:

        calibration_data = [
            ["Equipment ID", "Last Calibration", "Next Due Date", "Status"]
        ]

        for record in period_calibration_records:
            calibration_data.append([
                str(record.get("equipment_id", "")),
                str(record.get("last_calibration_date", "")),
                str(record.get("next_due_date", "")),
                str(record.get("status", ""))
            ])

        calibration_table = Table(
            calibration_data,
            colWidths=[90, 125, 125, 135],
            repeatRows=1
        )

        calibration_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))

        content.append(calibration_table)

    else:
        content.append(Paragraph(
            "No calibration records found in this period.",
            styles["Normal"]
        ))

    content.append(Spacer(1, 25))

    content.append(Paragraph(
        "CalibraLab - Laboratory Equipment Management System",
        styles["Italic"]
    ))

    document.build(content)
    pdf_buffer.seek(0)

    file_name = (
        "CalibraLab_Report_"
        + start.strftime("%Y%m%d")
        + "_to_"
        + end.strftime("%Y%m%d")
        + ".pdf"
    )

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=file_name,
        mimetype="application/pdf"
    )


# RUN APPLICATION

if __name__ == "__main__":
    app.run(debug=True)
