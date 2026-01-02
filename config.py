from os_utils import OSUtils

OS = OSUtils()

TASK_COLUMNS = [
    "Priority",
    "Tasks",
    "Sub tasks",
    "Status",
    "Comment",
    "Deadline_csv",
    "Deadline",
]

RECURRING_TASK_COLUMNS = ["Tasks", "Frequency"]


STATUS_CATEGORIES = (
    "Not started",
    "In progress",
    "Completed",
)

PRIORITY_CATEGORIES = (
    "Do it now!",
    "Decide when to do it.",
    "Delegate!",
    "Do it later/dump it!",
)

DATE_CATEGORIES = {
    "Overdue": 0,
    "Today": 1,
    "This week": 2,
    "Date range": 3,
}

# for text formatting
FORMAT_OPTIONS = 15
FORMAT_INPUT = 30


# dd-mm-yyyy hh:mm AM/PM
DATETIME_FORMAT = "%d-%m-%Y %I:%M %p"

# filenames
TODO_FILENAME = "tasks.csv"
RECURRING_FILENAME = "recurring.csv"

# pdf path
# pdf_path = '' for Desktop
# Eg.  'C:/Users/usr1/Desktop'
PDF_PATH = OSUtils.cwd()[:-1]
# PDF_PATH = ""
print(PDF_PATH)

# export pdf categories
PDF_CATEGORIES = {
    "all": "1",
    "overdue": "9",
    "today": "10",
    "week": "11",
}


# command line text for invalid display
def invalid_choice(second_line=" Try again. "):
    return input("\nInvalid choice." + second_line + "press 'Enter' to continue")


def input_format(text_str: str, choice_option="", input_=False, new_line=False):
    print_txt = f"{text_str:{FORMAT_INPUT}} : {choice_option}"

    if new_line:
        print()

    if input_:
        return input(print_txt)
    else:
        print(print_txt)


def options_format(text_str: str, choice_option="", input_=False, new_line=False):

    print_txt = f"{f"{text_str}":{FORMAT_OPTIONS}} : {choice_option}"

    if new_line:
        print()

    if input_:
        return input(print_txt)
    else:
        print(print_txt)
