from config import *
from deadlines import DeadlineUtils
from cli_menus import CLI_menus

# to avoid circular imports and make use of autofill
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task_manager import TaskManager


# =======================================================
# =======================================================


def task_ids_with_task_description(task: str, manager: "TaskManager") -> list:
    """
    return list of IDs of task/sub-tasks matching 'task'

    :param task: task description
    :type task: str
    :param manager: to handle tasks_df
    :type manager: "TaskManager"
    :return: list of IDs with task description = 'task'
    :rtype: list[int]
    """

    df = manager.tasks_df[manager.tasks_df["Tasks"] == task]

    return df.index.tolist()


# =======================================================
# =======================================================


def add_rows_tasks_df(data: list, manager: "TaskManager"):
    """
    append the tasks data to the database and tasks_df

    :param data: tasks data: [[task 1 data], [task 2 data], ...]
    :type data: list
    :param manager: to handle storage and tasks_df
    :type manager: "TaskManager"
    """

    # add rows to tasks_df
    for row in data:
        idx = len(manager.tasks_df)
        manager.tasks_df.loc[idx] = row

    # update tasks_dict
    manager.update_dict()
    # update database
    manager.storage.save_database(manager.tasks_df)

    return None


# =======================================================
# =======================================================


def add_sub_task(priority: str, task: str, no_sub_tasks: bool = False) -> list:
    """
    take details of task from user and return task data.

    :param priority: priority
    :type priority: str
    :param task: task description
    :type task: str
    :param no_sub_tasks: True if there are no sub tasks, otherwise False
    :type no_sub_tasks: bool
    :return: [priority, task, sub_task, status, comment, deadline_csv, deadline]
    :rtype: list
    """

    # sub task
    if not no_sub_tasks:
        sub_task = input_format("Enter sub-task", input_=True, new_line=True)
    # no sub task
    else:
        sub_task = "---"

    # deadline date details
    # default: today
    CLI_menus.show_deadline_date_menu()
    date_str = input_format("Enter date", input_=True, new_line=True)

    # deadline time details
    # default: 11:59 PM
    CLI_menus.show_deadline_time_menu()
    time_str = input_format("Enter time", input_=True, new_line=True)

    # status details
    # default: Not Started
    CLI_menus.show_status_menu()
    status_choice = input_format(
        "Status choice (1-3 or 'Enter')", input_=True, new_line=True
    )

    if status_choice in ["1", "2", "3"]:
        status = STATUS_CATEGORIES[int(status_choice) - 1]
    else:
        # default status
        status = STATUS_CATEGORIES[0]

    # comment details
    CLI_menus.show_comment_menu(priority)
    comment_choice = input_format(
        "Comment choice (1, 2, or 'Enter')", input_=True, new_line=True
    )

    # comment details. see CLI_menus.show_comment_menu for details
    # default: "---"
    if comment_choice not in ["1", "2"]:
        comment = "---"
    else:
        if priority == PRIORITY_CATEGORIES[0]:
            if comment_choice == "1":
                comment = "Do it now"
            else:
                comment = input_format("Enter comment", input_=True, new_line=True)
        elif priority == PRIORITY_CATEGORIES[1]:
            comment_prefix = "schedule: " if comment_choice == "1" else ""
            comment = input_format("Enter comment", input_=True, new_line=True)
            comment = comment_prefix + comment

        elif priority == PRIORITY_CATEGORIES[2]:
            comment_prefix = "delegate to " if comment_choice == "1" else ""
            comment = input_format("Enter comment", input_=True, new_line=True)
            comment = comment_prefix + comment
        else:
            if comment_choice == "1":
                comment = "Do it later"
            else:
                comment = "Dump it"

    # calculate deadline_csv and deadline
    deadline_csv = DeadlineUtils.deadline_csv_clean_up(date_str, time_str)
    deadline = DeadlineUtils.datetime_str_to_deadline_column(deadline_csv, status)

    data = [priority, task, sub_task, status, comment, deadline_csv, deadline]

    # show the details of added task/sub-task
    CLI_menus.sub_tasks_header([data])
    print("\nTask added.")

    return data


# =======================================================
# =======================================================


def add_tasks(manager: "TaskManager"):
    """
    Docstring for add_tasks

    :param manager: Description
    :type manager: "TaskManager"
    """

    while True:
        OS.clear_screen()

        task = input_format("\nEnter task description", input_=True)

        # if it is [], new task. else, already existing task
        task_check_exist_list = task_ids_with_task_description(task, manager)

        # already existing task
        if not task_check_exist_list == []:

            # 1. update task
            # 2. add new task
            # 3. return to Main Menu
            CLI_menus.show_task_exists_menu(task, task_check_exist_list[0])

            choice = int(input_format("\nEnter your choice (1-3)", input_=True))

            # 1. update task
            if choice == 1:
                return manager.update_tasks()
            # 2. add new task
            elif choice == 2:
                continue
            # 3. return to Main Menu
            else:
                return None

        # new task

        important = input_format("important (y/n)", input_=True, new_line=True)
        urgent = input_format("urgent (y/n)", input_=True)

        important = True if important.lower() == "y" else False
        urgent = True if urgent.lower() == "y" else False

        # The Eisenhower Matrix: Prioritizing tasks and to-do lists
        if important and urgent:
            priority_idx = 0
        elif important and not urgent:
            priority_idx = 1
        elif not important and urgent:
            priority_idx = 2
        else:
            priority_idx = 3

        # priority
        priority = PRIORITY_CATEGORIES[priority_idx]

        # show priority
        input_format("Priority", priority, new_line=True)

        choice_sub_task = input_format(
            "Add sub tasks (y/n)", input_=True, new_line=True
        )
        # False -> there are sub tasks
        no_sub_tasks = False if choice_sub_task.lower() == "y" else True

        # print priority and task description
        CLI_menus.sub_tasks_header([[priority, task]])

        tasks_list = []

        while True:
            # get task/sub-task data
            task_data = add_sub_task(priority, task, no_sub_tasks)
            # append data to tasks_list
            tasks_list.append(task_data)

            # no sub-task, exit
            if no_sub_tasks:
                break
            # repeat the process if there are sub-tasks
            else:
                add_sub_task_choice = input_format(
                    "Add more sub-tasks? (y/n)", input_=True, new_line=True
                )
                if add_sub_task_choice.lower() == "y":

                    CLI_menus.sub_tasks_header(tasks_list)
                else:
                    break

        # add data to tasks_df, database
        add_rows_tasks_df(tasks_list, manager)

        # recurring task
        recurring_task = input_format(
            "Is this a recurring task? (y/n)", input_=True, new_line=True
        )

        # update recurring task database, rec_dict
        if recurring_task.lower() == "y":
            frequency = input_format(
                "Enter frequency (in days)", input_=True, new_line=True
            )

            manager.RM.add_rec_task(task, frequency)

        choice = input_format("Add more tasks? (y/n)", input_=True, new_line=True)

        if not choice.lower() == "y":
            break

    return None


if __name__ == "__main__":

    OS.clear_screen()

    from storage import StorageManager
    from task_manager import TaskManager

    SM = StorageManager()
    TM = TaskManager(SM)

    print("task_ids_with_task_description:\n")
    task = "task_10"
    task_id_list = task_ids_with_task_description(task, TM)
    print(task_id_list)
    print("\nExiting task_ids_with_task_description\n")

    print("task_ids_with_task_description:\n")
    data = [
        [
            "Do it now!",
            "task_1",
            "---",
            "In progress",
            "comment_1",
            "23-12-2025 11:13 PM",
            "Overdue: 10 days ago",
        ],
        [
            "Delegate!",
            "task_2",
            "---",
            "Not started",
            "comment_2",
            "24-12-2025 11:13 PM",
            "Overdue: 9 days ago",
        ],
        [
            "Decide when to do it.",
            "task_3",
            "---",
            "Not started",
            "comment_3",
            "25-12-2025 11:13 PM",
            "Overdue: 8 days ago",
        ],
    ]
    add_rows_tasks_df(data, TM)
    print("\nExiting task_ids_with_task_description\n")

    print("add_tasks:\n")
    add_tasks(TM)
    print("\nExiting add_tasks\n")
