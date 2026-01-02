from config import OS, PDF_PATH, PDF_CATEGORIES
from show_tasks import show_tasks

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# to avoid circular imports and make use of autofill
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task_manager import TaskManager


# generate pdf of task with category = 'category'
def export_tasks_category(manager, category="overdue"):

    # get dataframe of 'category'
    data = show_tasks(manager, get_df=True, category=category)

    # pdf colors
    color_dict = {
        "all": ("#1F4ED8", "#D6E4FF"),
        "overdue": ("#B91C1C", "#FEE2E2"),
        "today": ("#EA580C", "#FFEDD5"),
        "week": ("#15803D", "#DCFCE7"),
    }
    heading_color, body_color = color_dict[category]

    # pdf save paths
    folder_path = OS.get_pdf_path(PDF_PATH)

    filename = folder_path + "ToDo_" + category + ".pdf"
    pdf = SimpleDocTemplate(filename=filename, pagesize=A4)

    # remove the 'ID' column
    # reset index
    data = data.reset_index()
    data = data.drop(columns=["ID"])

    table_data = []
    table_data.append(list(data.columns))

    # replace '---' with ''
    if len(data):
        row_data = data.iloc[0, :].tolist()
        row_data = [
            "" if row_data[i] == "---" else row_data[i] for i in range(len(row_data))
        ]
        table_data.append(row_data)

    # replace repeating priority, task with ''
    for i in range(1, len(data)):
        row_data = data.iloc[i, :].tolist()
        row_data = [
            "" if row_data[i] == "---" else row_data[i] for i in range(len(row_data))
        ]

        for col in range(2):
            if row_data[col] == data.iloc[i - 1, col]:
                row_data[col] = ""

        table_data.append(row_data)

    table = Table(table_data)

    # table style
    table_style = TableStyle(
        [
            # heading
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(heading_color)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
            # body
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor(body_color)),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
            ("ALIGN", (0, 1), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ]
    )

    table.setStyle(table_style)

    pdf_table = [table]

    # create pdf
    pdf.build(pdf_table)
    return None


# generate pdf of three categories of tasks
def export_tasks(manager: "TaskManager"):

    for category in PDF_CATEGORIES.keys():
        export_tasks_category(manager, category)

    return None


if __name__ == "__main__":

    OS.clear_screen()

    from storage import StorageManager
    from task_manager import TaskManager

    SM = StorageManager()
    TM = TaskManager(SM)

    export_tasks(TM)
