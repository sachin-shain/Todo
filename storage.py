import pandas as pd

pd.set_option("future.no_silent_downcasting", True)
import numpy as np
from config import *
from deadlines import DeadlineUtils


class StorageManager:
    """Handles CSV read/write operations
    members:
        file_names
        file_headers

    functions:
        check_for_databases()
        update_deadline_column()
        load_databases()
        close_database(tasks_df=None)
        save_database(tasks_df)
        load_recurring_df()
        save_recurring_df(r_df)
    """

    file_names = [TODO_FILENAME, RECURRING_FILENAME]
    file_headers = [TASK_COLUMNS, RECURRING_TASK_COLUMNS]

    # =======================================================
    # =======================================================

    # check whether the databases exists
    # update deadline columns of databases
    def __init__(self):

        # check for database and update deadline column
        self.check_for_databases()
        self.update_deadline_column()

    # =======================================================
    # =======================================================

    # call when StorageManager starts.
    # load databases if they exits, otherwise make empty databases
    def check_for_databases(self):

        # check for databases, create them if they do not exist
        for file_name, header in zip(self.file_names, self.file_headers):
            if not OS.check_file_exists(file_name):
                pd.DataFrame(columns=header).to_csv(file_name, index=False)

        return None

    # =======================================================
    # =======================================================

    # recalculate the deadline columns based on today's date
    def update_deadline_column(self):

        # read from database
        df = self.load_databases()

        # update deadline columns
        df["Deadline"] = df["Deadline_csv"].apply(
            DeadlineUtils.datetime_str_to_deadline_column
        )

        # if the status is 'Completed', remove Overdue prefix
        mask = (df["Status"] == STATUS_CATEGORIES[2]) & df["Deadline"].str.startswith(
            "Overdue: ", na=False
        )
        df.loc[mask, "Deadline"] = df.loc[mask, "Deadline"].str.replace(
            r"^Overdue: ", "", regex=True
        )

        # update database
        self.save_database(df)

        return None

    # =======================================================
    # =======================================================

    # read databases tasks and return them as DataFrames
    def load_databases(self):

        tasks_df = pd.read_csv(TODO_FILENAME)

        # replace empty data with '---'
        tasks_df = tasks_df.replace({np.nan: "---"})

        # return task_df dataframe
        return tasks_df

    # =======================================================
    # =======================================================

    # calls when program exists
    # save member DataFrames to csv (optional) and make them hidden
    def close_database(self, tasks_df=pd.DataFrame()):

        # save member DataFrames to csv
        if not tasks_df.empty:
            self.save_database(tasks_df)
        else:
            print(
                "\nProvided empty Database. Fix the issue. Terminating function close_database()"
            )
            return None

        return None

    # =======================================================
    # =======================================================

    # save member DataFrames to csv
    def save_database(self, tasks_df):

        tasks_df_copy = tasks_df.replace({"---": np.nan})
        tasks_df_copy.to_csv(TODO_FILENAME, index=False)

        return None

    # =======================================================
    # =======================================================

    # get recurring dataframe
    def load_recurring_df(self):
        recurring_df = pd.read_csv(RECURRING_FILENAME)
        return recurring_df

    # =======================================================
    # =======================================================

    # save to recurring.csv
    def save_recurring_df(self, r_df):
        r_df.to_csv(RECURRING_FILENAME, index=False)
        return None


if __name__ == "__main__":

    OS.clear_screen()
    SM = StorageManager()

    # print("check_for_databases:\n")
    # SM.check_for_databases()
    # input("\npress enter to continue")

    # print("update_deadline_column:\n")
    # SM.update_deadline_column()
    # input("\npress enter to continue")

    # print("load_databases:\n")
    # df = SM.load_databases()
    # print(df.head())
    # input("\npress enter to continue")

    # print("close_database:\n")
    # SM.close_database(df)
    # input("\npress enter to continue")

    # print("save_database:\n")
    # SM.save_database(df)
    # input("\npress enter to continue")

    # print("entering load_recurring_df:\n")
    # r_df = SM.load_recurring_df()
    # print(r_df)
    # print("exiting load_recurring_df\n")

    # input("entering save_recurring_df:\n")
    # SM.save_recurring_df(r_df)
    # print(r_df)
    # input("exiting save_recurring_df\n")
