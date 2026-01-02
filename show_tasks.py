from cli_menus import CLI_menus
from config import *
from deadlines import DeadlineUtils
import pandas as pd

# to avoid circular imports and make use of autofill
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task_manager import TaskManager


# print dataframe in a formatted way
# return the formatted dataframe if return_df = True
def print_df(df: pd.DataFrame, manager: "TaskManager", return_df=False):
    """
    Print the dataframe in a formatted way.

    Args:
        df (pd.DataFrame): data that need to be printed
        manager (TaskManger): to access tasks_dict

    Returns:
        None:
    """
    if df.empty:
        print("No tasks found!")
        return None

    key_list = []

    # list of (priority, task, sub task) keys of df
    for row in df.values:
        key = tuple(row[i] for i in range(3))
        key_list.append(key)

    # sorting the key by priority column
    priority_order = {priority: i for i, priority in enumerate(PRIORITY_CATEGORIES)}

    # list of all tasks
    task_list = df["Tasks"].tolist()

    # remove duplicate tasks, since sub-tasks have the same task name
    task_list = list(dict.fromkeys(task_list))

    # order the last in the order of input to database
    task_order = {task: i for i, task in enumerate(task_list)}

    # key_listed sorted by (priority_order, task_order)
    keys_sorted = sorted(
        key_list,
        key=lambda x: (
            priority_order.get(x[0], len(priority_order)),
            task_order.get(x[1], len(task_order)),
        ),
    )

    # multi_index : (priority, tasks, sub tasks)
    multi_index = pd.MultiIndex(
        levels=[[], [], []],
        codes=[[], [], []],
        names=TASK_COLUMNS[:3],
    )

    # columns : ID, status, comment, deadline,
    columns = ["ID"] + list(TASK_COLUMNS[3:])
    df1 = pd.DataFrame(index=multi_index, columns=columns)

    for key in keys_sorted:
        value = manager.tasks_dict[key]
        df1.loc[key] = value

    df1 = df1.drop(columns=["Deadline_csv"])

    if return_df:
        return df1
    else:
        print(df1)
        return None


# print recurring tasks
# add Frequency to index key
def print_recurring_tasks(manager: "TaskManager"):

    r_dict = manager.RM.rec_dict

    df1 = manager.tasks_df
    df1 = df1[df1["Tasks"].isin(r_dict.keys())]

    df2 = print_df(df1, manager, True)
    df3 = df2.reset_index()
    df3["Frequency"] = df3["Tasks"].map(r_dict)

    df3 = df3.set_index(["Priority", "Tasks", "Frequency", "Sub tasks"])

    OS.clear_screen()
    print(df3)

    return None


def show_tasks(manager: "TaskManager", get_df=False, category="overdue"):
    """
    print task according to various filters

    :param manager: to handle tasks_df, tasks_dict
    :type manager: "TaskManager"

    :param get_df: if true, return formatted df of categories
    :type get_df: bool

    :param category: category for export pdf: overdue, today, week
    :type category: str
    """

    while True:
        df = manager.tasks_df.copy()

        # choice depends on category
        if get_df:
            choice = PDF_CATEGORIES[category]
        # continue to show tasks menu
        else:

            if df.empty:
                input("\nNo tasks. press 'Enter' to continue ")
                break

            CLI_menus.show_print_menu()

            choice = input_format("\nEnter your choice (1-14)", input_=True)

        # Default choice
        if choice == "":
            choice = 1

        # check for valid choices
        elif choice.isdigit():
            choice = int(choice)
            if not (1 <= choice and choice <= 14):
                input("\nInvalid choice. Try again.")
                continue
        else:
            invalid_choice()
            continue

        # choice is between 1 and 13
        if choice == 1:
            pass
        elif choice in [2, 3, 4, 5]:
            df = df[df["Priority"] == PRIORITY_CATEGORIES[choice - 2]]

        elif choice in [6, 7, 8]:
            df = df[df["Status"] == STATUS_CATEGORIES[choice - 6]]

        elif choice in [9, 10, 11]:
            deadline_type = {
                9: r"Overdue:",
                10: r"Today ",
                11: r"\wday",
                20: r"\wday|Tom",
            }

            # if today is not sunday, then tomorrow is part of current week
            # need to include tomorrow while showing week days filter
            if choice == 11 and DeadlineUtils.today_get_weekday() != 7:
                choice = 20

            pattern = deadline_type[choice]

            df = df[df["Deadline"].str.contains(pattern, regex=True, na=False)]

        elif choice == 12:

            date_start = input(f'\n{"Enter start date (dd-mm-yyyy)":{FORMAT_INPUT}} : ')
            date_end = input(f'\n{"Enter end date (dd-mm-yyyy)":{FORMAT_INPUT}} : ')

            check_date_in_range_fun = DeadlineUtils.check_date_in_range_fun_gen(
                date_start, date_end
            )

            df = df[df["Deadline_csv"].apply(check_date_in_range_fun)]

        elif choice == 13:

            print_recurring_tasks(manager)

        else:
            # to exit to Main Menu, choice = 14
            return None

        # return df
        if get_df:
            # if df is empty return a en empty dataset with appropriate columns
            if df.empty:
                header = (
                    TASK_COLUMNS[:3] + ["ID"] + [TASK_COLUMNS[i] for i in [3, 4, 6]]
                )
                df1 = pd.DataFrame(columns=header)
                return df1

            # if df is not empty, return formatted df using print_df
            return print_df(df, manager, return_df=True)
        # continue to show tasks menu
        else:

            if choice != 13:
                OS.clear_screen()
                print_df(df, manager)

            choice_show_again = input_format(
                "\nWant to print again? ('Enter' or 'y' for yes/n)", input_=True
            )

            if choice_show_again.lower() == "y" or choice_show_again.lower() == "":
                continue
            else:
                # to exit to Main Menu
                return None


if __name__ == "__main__":

    OS.clear_screen()

    from storage import StorageManager
    from task_manager import TaskManager

    SM = StorageManager()
    TM = TaskManager(SM)

    show_tasks(TM)
