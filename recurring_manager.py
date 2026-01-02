from config import *
from deadlines import DeadlineUtils

# to avoid circular imports and make use of autofill
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task_manager import TaskManager


class RecurringManager:
    """
    manage recurring tasks

    variables:
        manager
        rec_df
        rec_dict

    functions:
        update_tasks_df()
        rec_dict_gen()
        add_rec_task(task, frequency)
        update_rec_task(task, frequency)
    """

    def __init__(self, manager: "TaskManager"):
        self.manager = manager

        self.rec_df = self.manager.storage.load_recurring_df()
        self.rec_dict_gen()

        self.update_tasks_df()

    # generate rec_dict
    def rec_dict_gen(self):
        self.rec_dict = {}

        for _, row in self.rec_df.iterrows():
            self.rec_dict[row["Tasks"]] = int(row["Frequency"])

        return None

    # update deadline for recurring tasks if the deadline elapsed
    def update_tasks_df(self):

        rec_task_list = self.rec_dict.keys()

        for idx, row in self.manager.tasks_df.iterrows():

            task, curr_deadline_str = row["Tasks"], row["Deadline_csv"]

            # only changes tasks in recurring.csv
            if task in rec_task_list and DeadlineUtils.task_deadline_elapsed(
                curr_deadline_str
            ):
                print(task in rec_task_list)
                print(DeadlineUtils.task_deadline_elapsed(curr_deadline_str))

                # new deadline is after today
                deadline_csv_new, deadline_new = (
                    DeadlineUtils.recurring_task_new_deadline(
                        curr_deadline_str, self.rec_dict[task]
                    )
                )
                self.manager.tasks_df.loc[idx, "Deadline_csv"] = deadline_csv_new
                self.manager.tasks_df.loc[idx, "Deadline"] = deadline_new
                self.manager.tasks_df.loc[idx, "Status"] = STATUS_CATEGORIES[0]

        # update tasks_dict
        self.manager.update_dict()
        # save tasks_df
        self.manager.storage.save_database(self.manager.tasks_df)

        return None

    # add recurring tasks and save to recurring.csv
    def add_rec_task(self, task, frequency):

        self.rec_df.loc[len(self.rec_df)] = [task, frequency]

        # update rec_dict
        self.rec_dict_gen()
        # update recurring.csv
        self.manager.storage.save_recurring_df(self.rec_df)

    # update recurring tasks and save to recurring.csv
    def update_rec_task(self, task, frequency):

        if task in self.rec_df["Tasks"].values:
            idx = self.rec_df[self.rec_df["Tasks"] == task].index[0]
            self.rec_df.loc[idx] = [task, int(frequency)]

        # update rec_dict
        self.rec_dict_gen()
        # update tasks_df
        self.update_tasks_df()
        # update recurring.csv
        self.manager.storage.save_recurring_df(self.rec_df)


if __name__ == "__main__":

    OS.clear_screen()

    from storage import StorageManager
    from task_manager import TaskManager

    SM = StorageManager()
    TM = TaskManager(SM)

    RM = RecurringManager(TM)

    print("entering update_tasks_df:\n")
    RM.update_tasks_df()
    print("Exiting update_tasks_df\n")

    print("entering rec_dict_gen:\n")
    RM.rec_dict_gen()
    print("Exiting rec_dict_gen\n")

    print("entering add_rec_task:\n")
    task, frequency = "task_2", 10
    RM.add_rec_task(task, frequency)
    task, frequency = "task_20", 5
    RM.add_rec_task(task, frequency)
    print("Exiting add_rec_task\n")

    print("entering update_rec_task:\n")
    input("press enter")
    task, frequency = "task_20", 30
    RM.update_rec_task(task, frequency)
    print("Exiting update_rec_task\n")
