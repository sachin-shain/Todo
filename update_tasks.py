from config import *
from deadlines import DeadlineUtils
from cli_menus import CLI_menus
from add_tasks import task_ids_with_task_description
from show_tasks import print_df

# to avoid circular imports and make use of autofill
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task_manager import TaskManager


# =======================================================
# =======================================================


def update_sub_task(task_id: int, manager: "TaskManager"):

    df = manager.tasks_df.loc[task_id]

    [priority, task, sub_task, status_curr, comment_curr, deadline_csv_curr] = (
        df.values[:-1]
    )

    # get current date and time
    datetime_obj = DeadlineUtils.datetime_str_to_datetime_obj(deadline_csv_curr)
    date_str_current = datetime_obj.strftime("%d-%m-%Y")
    time_str_current = datetime_obj.strftime("%I:%M %p")

    # update date
    CLI_menus.show_deadline_date_menu(update=True, date_str=date_str_current)
    date_str = input_format("Enter date", input_=True, new_line=True)
    if date_str == "":
        date_str = date_str_current

    # update time
    CLI_menus.show_deadline_time_menu(update=True, time_str=time_str_current)
    time_str = input_format("Enter time", input_=True, new_line=True)
    if time_str == "":
        time_str = time_str_current

    # update status
    CLI_menus.show_status_menu(update=True, status=status_curr)

    status_choice = input_format(
        "Status choice (1-3 or 'Enter')", input_=True, new_line=True
    )

    if status_choice in ["1", "2", "3"]:
        status = STATUS_CATEGORIES[int(status_choice) - 1]
    else:
        status = status_curr

    # update comment
    CLI_menus.show_comment_menu(priority, update=True, comment=comment_curr)

    comment_choice = input_format(
        "Comment choice (1, 2, or 'Enter')", input_=True, new_line=True
    )

    if comment_choice not in ["1", "2"]:
        comment = comment_curr
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

    # updated deadline,
    deadline_csv = DeadlineUtils.deadline_csv_clean_up(date_str, time_str)
    deadline = DeadlineUtils.datetime_str_to_deadline_column(deadline_csv, status)

    data = [priority, task, sub_task, status, comment, deadline_csv, deadline]

    # update tasks_df
    manager.tasks_df.loc[task_id] = data

    # update tasks_dict
    manager.update_dict()

    # print updated task details
    OS.clear_screen()
    CLI_menus.sub_tasks_header([data])
    print("\nTask updated.\n")

    return None


# =======================================================
# =======================================================


def update_tasks(manager: "TaskManager"):
    while True:

        # show task/sub-tasks description and ID
        CLI_menus.show_task_id(manager.tasks_dict)

        task_id = int(
            input_format("Enter task/sub-task ID : ", input_=True, new_line=True)
        )

        task = manager.tasks_df.loc[task_id, "Tasks"]
        task_id_list = task_ids_with_task_description(task, manager)

        if task_id_list == []:
            invalid_choice()
            continue

        tasks_id_df = manager.tasks_df.loc[task_id_list]

        # print task description
        CLI_menus.sub_tasks_header(tasks_id_df.values)

        update_sub_task(task_id, manager)

        while len(tasks_id_df) > 1:

            choice = input_format(
                "Want to update more sub-tasks? (y/n)", input_=True, new_line=True
            )

            if choice.lower() == "y":
                # print task description
                OS.clear_screen()
                print_df(tasks_id_df, manager)
                # CLI_menus.sub_tasks_header(tasks_id_df.values)

                sub_task_id = int(
                    input_format("Enter sub-task id", input_=True, new_line=True)
                )

                update_sub_task(sub_task_id, manager)
            else:
                break

        manager.storage.save_database(manager.tasks_df)

        if task in manager.RM.rec_dict.keys():
            update_frequency = input_format(
                "Want to change frequency? (y/n)", input_=True, new_line=True
            )

            if update_frequency.lower() == "y":
                frequency_new = input_format(
                    "Enter frequency (in days)", input_=True, new_line=True
                )

                manager.RM.update_rec_task(task, frequency_new)

        choice = input_format(
            "Want to update more tasks? (y/n)", input_=True, new_line=True
        )

        if choice.lower() == "y":
            continue
        else:
            break

    return None
