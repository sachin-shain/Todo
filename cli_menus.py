from config import *
import pandas as pd


class CLI_menus:
    """
    Docstring for CLI_menus

    functions (staticmethod):
        show_main_menu()
        sub_tasks_header(tasks_list, update=None, idx_list=None)
        show_deadline_date_menu(update=False, date_str=None)
        show_deadline_time_menu(update=False, time_str=None)
        show_status_menu(update=False, status=None)
        show_comment_menu(priority, update=False, comment=None)
        show_update_menu()
        show_print_menu()
        show_task_id(tasks_dict)
        show_task_exists_menu(task, task_id)
        show_delete_menu()

    """

    def __init__(self, testing=False):
        # testing
        self.testing = testing
        pass

    # =======================================================
    # =======================================================

    @staticmethod
    def show_main_menu():

        OS.clear_screen()

        print("\tMain menu")
        options_list = [
            "Add task",
            "Show tasks",
            "Update tasks",
            "Delete tasks",
            "Quit",
        ]

        for idx, options in enumerate(options_list):
            options_format(options, idx + 1)

        return None

    # =======================================================
    # =======================================================

    # task_list = [[priority, task]]
    # task_list = [[priority, task, sub task, status, comment, deadline_csv, deadline],...]
    # update = True:
    #   rename the index with 'ID' and its values with idx_list
    @staticmethod
    def sub_tasks_header(tasks_list, update=False, idx_list=None):

        OS.clear_screen()

        options_format("Priority", tasks_list[0][0])
        options_format("Task", tasks_list[0][1])

        # while entering the task/ first sub-task : [[priority, task]]
        if len(tasks_list[0]) == 2:
            return None

        sub_tasks_list = []

        # only print columns : [Sub tasks, Status, Comment,Deadline]

        for task_data in tasks_list:
            sub_task_data = [task_data[i] for i in [2, 3, 4, 6]]
            sub_tasks_list.append(sub_task_data)

        header = [TASK_COLUMNS[i] for i in [2, 3, 4, 6]]
        df = pd.DataFrame(sub_tasks_list, columns=header)

        # if update = True, name the index as 'ID'
        #   use idx_values as index values
        if update:
            df.index = idx_list
            df.index.name = "ID"
        print()
        print(df)

        return None

    # =======================================================
    # =======================================================

    # update = False => Default : Today
    # update = True  => Default : date_str
    @staticmethod
    def show_deadline_date_menu(update=False, date_str=None):
        print("\nEnter deadline: date")

        options_list = [
            "Format",
            "",
            "",
            "",
            "",
        ]

        options_choice_list = [
            "dd-mm-yyyy",
            "monday/mon-sunday/sun",
            "today/tod",
            "tomorrow/tom",
            "none: today + 1 year (no deadline)",
        ]

        for option, option_choice in zip(options_list, options_choice_list):
            options_format(option, option_choice)

        if update:
            default = date_str
        else:
            default = "today"

        options_format("Default", default + " (press 'Enter')")

        return None

    # =======================================================
    # =======================================================

    # update = False => Default : 11:59 PM
    # update = True  => Default : time_str
    @staticmethod
    def show_deadline_time_menu(update=False, time_str=None):
        print("\nEnter deadline: time")

        options_format("Format", "hh:mm am/pm")

        if update:
            default = time_str
        else:
            default = "11:59 PM"

        options_format("Default", default + " (press 'Enter')")

        return None

    # =======================================================
    # =======================================================

    # update = False => Default : Not started
    # update = True  => Default : status
    @staticmethod
    def show_status_menu(update=False, status=None):
        print("\n\tStatus Options")

        for idx, option in enumerate(STATUS_CATEGORIES):
            options_format(option, idx + 1)
        if update:
            default = status
        else:
            default = STATUS_CATEGORIES[0]

        options_format("Default", default + " (press 'Enter')")

        return None

    # =======================================================
    # =======================================================

    # update = False => Default : ---
    # update = True  => Default : comment
    @staticmethod
    def show_comment_menu(priority, update=False, comment=None):

        print("\nEnter Comment:")

        priority_idx = PRIORITY_CATEGORIES.index(priority)

        option_1_list = [
            "for 'Do it now'",
            "for prefix 'schedule: '",
            "for prefix 'delegate to '",
            "for 'Do it later'",
        ]

        option_2_list = ["no prefix", "no prefix", "no prefix", "for 'Dump it'"]

        option_1, option_2 = option_1_list[priority_idx], option_2_list[priority_idx]
        input_format(option_1, 1)
        input_format(option_2, 2)

        if update:
            default = comment
        else:
            default = "---"
        input_format("Default", default + " (press 'Enter')")

        return None

    # =======================================================
    # =======================================================

    @staticmethod
    def show_update_menu():
        OS.clear_screen()
        print("\t\tUpdate Menu")

        options_list = ["Add sub tasks", "Update tasks/sub-tasks", "Exit to Main Menu"]
        options_choice_list = ["1", "2", "press 'Enter'"]
        for option, option_choice in zip(options_list, options_choice_list):
            input_format(option, option_choice)

        return None

    # =======================================================
    # =======================================================

    @staticmethod
    def show_print_menu():
        OS.clear_screen()
        print("\n\tPrint Menu")

        input_format("All", "1 (press Enter)")

        print("\nPriority:\n")

        for i, priority in enumerate(PRIORITY_CATEGORIES):
            input_format(priority, i + 2)

        print("\nStatus:\n")

        for i, status in enumerate(STATUS_CATEGORIES):
            input_format(status, i + 6)

        print("\nDeadline:\n")

        options_list = ["Overdue", "Today", "This week", "Date Range"]

        for idx, option in enumerate(options_list):
            input_format(option, idx + 9)

        input_format("Recurring tasks", 13, new_line=True)

        input_format("Main Menu", 14, new_line=True)

        return None

    # =======================================================
    # =======================================================

    # print ID, task, sub task
    # dict -> (priority, task, sub task) : ID, status, comment, deadline_csv, deadline
    @staticmethod
    def show_task_id(tasks_dict):

        OS.clear_screen()

        header = TASK_COLUMNS[1:3]
        df = pd.DataFrame(columns=header)

        # key [1:] -> (task, sub task)
        # value[0] -> ID
        # df -> ID : [task, sub task]
        for key, value in tasks_dict.items():
            df.loc[value[0]] = key[1:]
        df.index.name = "ID"

        print(df)

        return None

    # =======================================================
    # =======================================================

    # to show when an entered task already exists in the database
    @staticmethod
    def show_task_exists_menu(task, task_id):

        print(f"\nThe task '{task}' (ID = {task_id}) already exists.")

        print("\nDo you want to")
        input_format("Update task", 1)
        input_format("Add another task", 2)
        input_format("Exit to main menu", 3)

        return None

    # =======================================================
    # =======================================================

    @staticmethod
    def show_delete_menu():

        OS.clear_screen()

        print("\tDelete Menu")

        input_format("Delete tasks using ID", 1)
        input_format("Delete 'Completed' non-recurring tasks", 2)
        input_format("Exit to main menu", "press 'Enter'")

        return None


if __name__ == "__main__":

    print("show_main_menu:")
    CLI_menus.show_main_menu()
    input("\nPress enter to continue")

    print("sub_tasks_header:")

    task_list_1 = [["Do it now!", "task_7"]]
    task_list_2 = [
        [
            "Do it later/dump it!",
            "task 4",
            "sub task 4.1",
            "Not started",
            "---",
            "26-12-2025 11:59 AM",
            "Overdue: Today 11:59 AM",
        ]
    ]
    task_list_3 = [
        [
            "Do it now!",
            "task_7",
            "sub_task_7_0",
            "In progress",
            "comment_7_0",
            "25-12-2025 09:07 AM",
            "Overdue: Yesterday 09:07 AM",
        ],
        [
            "Do it now!",
            "task_7",
            "sub_task_7_1",
            "Not started",
            "comment_7_1",
            "25-12-2025 11:59 PM",
            "Overdue: Yesterday 11:59 PM",
        ],
        [
            "Do it now!",
            "task_7",
            "sub_task_7_2",
            "Completed",
            "comment_7_2",
            "26-12-2025 08:57 AM",
            "Overdue: Today 08:57 AM",
        ],
        [
            "Do it now!",
            "task_7",
            "sub_task_7_3",
            "In progress",
            "comment_7_3",
            "26-12-202509:02 AM",
            "Overdue: Today 09:02 AM",
        ],
    ]

    count = 1
    for tasks_list in [task_list_1, task_list_2, task_list_3]:
        print(f"tasks list: {count}")
        count += 1
        CLI_menus.sub_tasks_header(tasks_list)
        input("\nPress enter to continue")

    print("show_deadline_date_menu:")
    CLI_menus.show_deadline_date_menu()
    CLI_menus.show_deadline_date_menu(update=True, date_str="01-02-2020")
    input("\nPress enter to continue")

    print("show_deadline_time_menu:")
    CLI_menus.show_deadline_time_menu()
    CLI_menus.show_deadline_time_menu(update=True, time_str="12:02 PM")
    input("\nPress enter to continue")

    print("show_status_menu")
    CLI_menus.show_status_menu()
    CLI_menus.show_status_menu(update=True, status=STATUS_CATEGORIES[1])
    input("\nPress enter to continue")

    print("show_comment_menu")
    for i in range(4):
        CLI_menus.show_comment_menu(priority=PRIORITY_CATEGORIES[i])
    for i in range(4):
        CLI_menus.show_comment_menu(
            priority=PRIORITY_CATEGORIES[i], update=True, comment="sample comment"
        )
    input("\nPress enter to continue")

    print("show_update_menu")
    CLI_menus.show_update_menu()
    input("\nPress enter to continue")

    print("show_print_menu")
    CLI_menus.show_print_menu()
    input("\nPress enter to continue")

    print("show_task_id")
    tasks_list_keys = tasks_dict = {
        ("Decide when to do it.", "task 1", "sub task 1.1"): [
            1,
            STATUS_CATEGORIES[1],
            "comment 1.1",
            "deadline 1.1 csv",
            "deadline 1.1",
        ],
        ("Decide when to do it.", "task 1", "sub task 1.2"): [
            2,
            STATUS_CATEGORIES[1],
            "comment 1.2",
            "deadline 1.2 csv",
            "deadline 1.2",
        ],
        ("Delegate!", "task 2", "sub task 2.1"): [
            21,
            STATUS_CATEGORIES[1],
            "comment 2.1",
            "deadline 2.1 csv",
            "deadline 2.1",
        ],
    }
    CLI_menus.show_task_id(tasks_list_keys)
    input("\nPress enter to continue")
