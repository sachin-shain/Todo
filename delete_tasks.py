from cli_menus import CLI_menus
from config import *
from show_tasks import print_df

# to avoid circular imports and make use of autofill
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task_manager import TaskManager
manager: "TaskManager"


# delete the task with the index = task_id
def delete_task_with_id(task_id: int, manager: "TaskManager"):
    manager.tasks_df = manager.tasks_df.drop(index=task_id)
    manager.update_dict()
    return None


# menu to delete tasks by entering the ID
def delete_task_from_id(manager: "TaskManager"):

    while True:
        OS.clear_screen()

        # empty tasks_df
        if len(manager.tasks_dict) == 0:
            input("\nNo tasks. Press 'Enter' to continue ")
            break

        # show task/sub-tasks description and ID
        CLI_menus.show_task_id(manager.tasks_dict)

        delete_task_id = input_format(
            "Enter task/sub-task ID", input_=True, new_line=True
        )

        # entering non-digits -> invalid input
        if not delete_task_id.isdigit():
            invalid_choice()
            continue

        task_id = int(delete_task_id)

        # task_id is not an index -> invalid choice
        if not (task_id in manager.tasks_df.index):
            invalid_choice()
            continue

        # get task description
        task = manager.tasks_df.loc[task_id, "Tasks"]
        # df with all tasks with same description (to get all sub-tasks)
        df = manager.tasks_df[manager.tasks_df["Tasks"] == task]

        # no sub-tasks
        if len(df) == 1:

            OS.clear_screen()

            # show task details
            print_df(df, manager)

            # delete task and update recurring.csv
            manager.RM.delete_rec_task(task_id)
            delete_task_with_id(task_id, manager)

            print(f"\nTask '{task}' deleted.")

        # has sub-tasks
        else:
            # to delete the sub task with entered ID
            flag = True
            while True:

                OS.clear_screen()
                # get task description
                df = manager.tasks_df[manager.tasks_df["Tasks"] == task]

                # print all subtasks with same task
                print_df(df, manager)

                if flag:
                    # entered task_id
                    subtask_id = task_id
                    flag = False
                else:
                    # when chose to delete more sub tasks from same task,
                    # this will appear

                    subtask_id = int(
                        input_format("Enter sub-task ID ", input_=True, new_line=True)
                    )
                # same procedure as before
                subtask = manager.tasks_df.loc[subtask_id, "Sub tasks"]

                delete_task_with_id(subtask_id, manager)

                print(f"\nSub-task '{subtask}' deleted.")

                # no more sub task after the current one is deleted
                if len(df) == 1:
                    input("\nNo more sub-task. press 'Enter' to continue")
                    break

                subtask_delete_choice = input_format(
                    "\nWant to delete more sub-tasks? (y/n)", input_=True
                )

                if subtask_delete_choice.lower() == "y":
                    continue
                else:
                    break

        # to delete more tasks
        task_delete_choice = input_format(
            "Want to delete more tasks? (y/n)", input_=True, new_line=True
        )

        if task_delete_choice.lower() == "y":
            continue
        else:
            break

    return None


def delete_tasks(manager: "TaskManager"):
    """
    delete tasks by
    1. ID
    2. completed task

    :param manager: to update tasks_df
    :type manager: "TaskManager"
    """

    if manager.tasks_df.empty:
        input("\nNo tasks. press 'Enter' to continue ")
        return None

    while True:

        CLI_menus.show_delete_menu()

        # 1. delete from ID
        # 2. delete Completed tasks
        # 3. Main Menu
        choice = input_format(
            "Enter you choice (1,2, or 'Enter')", input_=True, new_line=True
        )

        # 1. delete from ID
        if choice == "1":
            delete_task_from_id(manager)

            # update database
            manager.storage.save_database(manager.tasks_df)

        # 2. delete Completed tasks
        elif choice == "2":
            df_completed = manager.tasks_df[manager.tasks_df["Status"] == "Completed"]
            df_completed_idx = df_completed.index

            # no 'Completed' tasks
            if df_completed.empty:
                input("\nNo 'Completed' tasks. press 'Enter to continue ")
                continue

            manager.tasks_df = manager.tasks_df.drop(index=df_completed_idx)
            manager.update_dict()

            input("\n'Completed' tasks were deleted. Press 'Enter' to continue ")

            # update database
            manager.storage.save_database(manager.tasks_df)

        else:
            break

    return None


if __name__ == "__main__":

    OS.clear_screen()

    from storage import StorageManager
    from task_manager import TaskManager

    SM = StorageManager()
    manager = TaskManager(SM)

    input("Entering delete_tasks:\n")
    delete_tasks(manager)
    print("\nExiting delete_tasks\n")
