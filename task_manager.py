from config import *
from storage import StorageManager
from pdf_exporter import export_tasks


from add_tasks import add_tasks
from update_tasks import *
from show_tasks import show_tasks
from delete_tasks import delete_tasks

from recurring_manager import RecurringManager


class TaskManager:
    """
    to manage tasks

    variables:
        tasks_df
        tasks_dict
        RM

    functions:
        update_dict()
        add_tasks()
        update_tasks()
        show_tasks()
        delete_tasks()
        exit_main_menu()

    """

    # row = [Priority,Tasks,Sub tasks,Status,Comment,Deadline_csv,Deadline]
    tasks_df = None
    # key = (Priority,Tasks,Sub)
    # value = (ID,Status,Comment,Deadline_csv,Deadline)
    tasks_dict = None

    def __init__(self, storage: StorageManager):
        self.storage = storage
        self.tasks_df = self.storage.load_databases()

        # create tasks_dict
        self.update_dict()

        self.RM = RecurringManager(self)

    # convert dataframe to dict in the form
    #   (Priority,Tasks,Sub): (ID,Status,Comment,Deadline_csv,Deadline)
    #   ID is the index of dataframe
    def update_dict(self):

        self.tasks_dict = dict()

        for idx, row in self.tasks_df.iterrows():
            key = tuple(row[col] for col in TASK_COLUMNS[:3])
            value = [idx]
            value += [row[col] for col in TASK_COLUMNS[3:]]
            self.tasks_dict[key] = value

        return None

    def add_tasks(self):
        add_tasks(self)

    def update_tasks(self):
        update_tasks(self)

    def show_tasks(self):
        show_tasks(self)

    def delete_tasks(self):
        delete_tasks(self)

    def exit_main_menu(self):
        # save tasks_df to database
        self.storage.save_database(self.tasks_df)
        export_tasks(self)


if __name__ == "__main__":

    SM = StorageManager()
    TM = TaskManager(SM)

    OS.clear_screen()

    # print("update_dict:")
    # TM.update_dict()
    # for key, values in TM.tasks_dict.items():
    #     print(f"{str(key):50} :  {values}")
    # input("\npress enter to continue")

    # print("add tasks:")
    # TM.add_tasks()
    # input("\npress enter to continue")

    # print("update_tasks:")
    # TM.update_tasks()
    # input("\npress enter to continue")

    # print("show_tasks:")
    # TM.show_tasks()
    # input("\npress enter to continue")

    # print("delete_tasks:")
    # TM.delete_tasks()
    # input("\npress enter to continue")

    # print("exit_main_menu:")
    # TM.exit_main_menu()
    # input("\npress enter to continue")
