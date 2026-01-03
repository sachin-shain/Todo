from config import OS, PDF_PATH, PDF_CATEGORIES
from show_tasks import show_tasks

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# to avoid circular imports and make use of autofill
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task_manager import TaskManager


# style the cell contents
def wrap_cell(text, style):
    if text is None:
        return ""
    return Paragraph(str(text), style)


# date in line 1, time in line 2
def deadline_col_format(txt):
    txt_list = txt.split()
    # text before time -> date, Overdue: date
    txt_1 = " ".join(txt_list[:-2])
    # time -> hh:mm PM
    txt_2 = " ".join(txt_list[-2:])
    # add line break between date and time
    return txt_1 + "<br/>" + txt_2


# generate pdf of task with category = 'category'
def export_tasks_category(manager, category="overdue"):

    # get dataframe of 'category'
    data = show_tasks(manager, get_df=True, category=category)

    # pdf save paths
    folder_path = OS.get_pdf_path(PDF_PATH)

    filename = folder_path + "ToDo_" + category + ".pdf"
    pdf = SimpleDocTemplate(filename=filename, pagesize=A4)

    # remove the 'ID' column
    # reset index
    data = data.reset_index()
    data = data.drop(columns=["ID"])

    # pdf colors
    color_dict = {
        "all": ("#1F4ED8", "#D6E4FF"),
        "overdue": ("#B91C1C", "#FEE2E2"),
        "today": ("#EA580C", "#FFEDD5"),
        "week": ("#15803D", "#DCFCE7"),
    }
    heading_color, body_color = color_dict[category]

    # pdf column width

    page_width, _ = A4

    # subtract margins if any
    usable_width = page_width - 2 * 40

    col_widths = [
        usable_width * 0.14,  # Priority
        usable_width * 0.20,  # Task
        usable_width * 0.20,  # Sub Task
        usable_width * 0.12,  # Status
        usable_width * 0.21,  # Comment
        usable_width * 0.13,  # Deadline
    ]

    # pdf heading and body styles
    header_style = ParagraphStyle(
        name="HeaderStyle",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=colors.whitesmoke,
        alignment=TA_CENTER,
    )

    body_style = ParagraphStyle(
        name="BodyStyle",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=colors.black,
        alignment=TA_LEFT,
        wordWrap="CJK",  # IMPORTANT for long text
    )

    table_data = []
    table_data.append([wrap_cell(col, header_style) for col in data.columns])

    # to make it look like the display of multi-level index dataframe display
    #   rows with same priority, task -> only keep the first line
    # replace "---" with ""
    # In deadline column, date in line 1 and time in line 2
    for i in range(len(data)):
        # heading, style the heading
        row_data = data.iloc[i, :].tolist()
        row_data = ["" if v == "---" else v for v in row_data]

        # rows with same priority, task -> only keep the first line
        if i > 0:
            for col in range(2):
                if row_data[col] == data.iloc[i - 1, col]:
                    row_data[col] = ""

        # In deadline column, date in line 1 and time in line 2
        row_data[-1] = deadline_col_format(row_data[-1])

        # style the body
        table_data.append([wrap_cell(v, body_style) for v in row_data])

    table = Table(
        table_data, colWidths=col_widths, repeatRows=1  # header repeats on page break
    )

    # table style
    table_style = TableStyle(
        [
            # heading
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(heading_color)),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
            # body
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor(body_color)),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 2),
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
