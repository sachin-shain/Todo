from datetime import datetime, timedelta
from config import DATETIME_FORMAT
import re


class DeadlineUtils:
    """Utility functions for handling deadlines

    functions (staticmethod):
        datetime_obj_to_datetime_str(datetime_obj) : str
        datetime_str_to_datetime_obj(datetime_str) : datetime
        datetime_str_to_deadline_column(datetime_str) : str
        deadline_csv_clean_up(date_str, time_str) : str
        date_clean_up(date_str) : str
        time_clean_up(time_str) : str
        check_date_in_range_fun_gen(date_start, date_end) : function
        today_get_weekday(): int
        task_deadline_elapsed(deadline_str): bool
        recurring_task_new_deadline(deadline_str, frequency): (str, str)

    """

    # convert datetime object to datetime string
    @staticmethod
    def datetime_obj_to_datetime_str(datetime_obj):
        return datetime_obj.strftime(DATETIME_FORMAT)

    # =======================================================
    # =======================================================

    # convert datetime string into datetime object
    @staticmethod
    def datetime_str_to_datetime_obj(datetime_str):
        return datetime.strptime(datetime_str, DATETIME_FORMAT)

    # =======================================================
    # =======================================================

    # give data for deadline column by giving deadline_csv value
    # deadline column
    #   deadline elapsed, add prefix 'Overdue'
    #   replace dates with Yesterday, Today, Tomorrow
    #   deadline is due on or before weekend (Sunday),
    #       use day name instead of date
    @staticmethod
    def datetime_str_to_deadline_column(datetime_str, status="Not started"):

        # convert to datetime object
        datetime_obj = DeadlineUtils.datetime_str_to_datetime_obj(datetime_str)

        # today datetime object
        today = datetime.today()

        # deadline_csv time string
        time_str = datetime.strftime(datetime_obj, "%I:%M %p")

        # remove time, convert to dates
        today_date = today.date()
        datetime_obj_date = datetime_obj.date()

        # ====== check if the deadline is today or overdue ======
        # overdue prefix only if task is not completed
        if status == "Completed":
            prefix = ""
        else:
            prefix = "Overdue: "

        # add prefix if deadline is elapsed
        if datetime_obj < today:
            # overdue, deadline was today
            if datetime_obj_date == today_date:
                deadline_str = prefix + "Today " + time_str
            # overdue, deadline was yesterday
            elif datetime_obj_date == today_date - timedelta(days=1):
                deadline_str = prefix + "Yesterday " + time_str
            # overdue, deadline was before yesterday
            else:
                deadline_str = (
                    f"{prefix}{(today_date - datetime_obj_date).days} days ago"
                )

        # deadline has not been elapsed
        else:

            # weekend with time set to midnight
            weekend = today + timedelta(days=7 - today.isoweekday())
            weekend = weekend.replace(hour=23, minute=59, second=0, microsecond=0)

            # deadline is today
            if datetime_obj_date == today_date:
                deadline_str = "Today " + time_str
            # deadline is tomorrow
            elif datetime_obj_date == today_date + timedelta(days=1):
                deadline_str = "Tomorrow " + time_str
            # deadline is in this week
            elif datetime_obj <= weekend:
                deadline_str = datetime.strftime(datetime_obj, "%A %I:%M %p")
            # deadline is after weekend
            else:
                deadline_str = datetime_str

        return deadline_str

    # =======================================================
    # =======================================================

    # return deadline_csv date from date and time input
    @staticmethod
    def deadline_csv_clean_up(date_str, time_str):

        date_str_cleaned = DeadlineUtils.date_clean_up(date_str)
        time_str_cleaned = DeadlineUtils.time_clean_up(time_str)

        # invalid input in date or time or both
        if not (date_str_cleaned and time_str_cleaned):
            return None
        # expected input
        else:
            datetime_str_unformatted = date_str_cleaned + " " + time_str_cleaned
            datetime_obj = DeadlineUtils.datetime_str_to_datetime_obj(
                datetime_str_unformatted
            )
            datetime_str = DeadlineUtils.datetime_obj_to_datetime_str(datetime_obj)

            return datetime_str

    # =======================================================
    # =======================================================

    # return date string from date input
    @staticmethod
    def date_clean_up(date_str):

        # "1-9-2024" (proper input)
        pattern = r"(\d{1,2}-\d{1,2}-\d{4})\s*$"
        match = re.search(pattern, date_str, re.IGNORECASE)

        if match:
            # remove trailing spaces
            extracted = match.group(1)
            return extracted

        # today/tod, tomorrow/tom, monday/mon-sunday/sun, ''(default)
        today = datetime.today()
        day_dict = {
            "monday": 1,
            "tuesday": 2,
            "wednesday": 3,
            "thursday": 4,
            "friday": 5,
            "saturday": 6,
            "sunday": 7,
            "tomorrow": (today + timedelta(days=1)).isoweekday(),
            "mon": 1,
            "tue": 2,
            "wed": 3,
            "thu": 4,
            "fri": 5,
            "sat": 6,
            "sun": 7,
            "tom": (today + timedelta(days=1)).isoweekday(),
        }

        date_str = date_str.lower()

        # today/tod, ''(default)
        if date_str in ["tod", "today", ""]:
            return datetime.strftime(today, "%d-%m-%Y")

        # tomorrow/tom, monday/mon-sunday/sun
        if date_str in day_dict.keys():

            days = day_dict[date_str] - today.isoweekday()
            if day_dict[date_str] <= today.isoweekday():
                days += 7

            return datetime.strftime(today + timedelta(days=days), "%d-%m-%Y")

        # none ==> today + 1 year
        if date_str == "none":
            date_obj = today + timedelta(days=365)
            return datetime.strftime(date_obj, "%d-%m-%Y")

        # invalid input
        return None

    # =======================================================
    # =======================================================

    # return time string from time input
    @staticmethod
    def time_clean_up(time_str):

        # "5:00 AM" (proper input)
        pattern = r"^(\d{1,2}:\d{1,2}\s(?:am|pm))\s*$"
        match = re.search(pattern, time_str, re.IGNORECASE)

        if match:
            # avoid the trailing spaces
            extracted = match.group(1)
            return extracted.upper()

        # default time = 11:59 AM
        if time_str == "":
            return "11:59 PM"

        # invalid input
        return None

    # =======================================================
    # =======================================================

    @staticmethod
    def check_date_in_range_fun_gen(date_start, date_end):

        datetime_start = DeadlineUtils.datetime_str_to_datetime_obj(
            date_start + " 12:00 AM"
        )
        datetime_end = DeadlineUtils.datetime_str_to_datetime_obj(
            date_end + " 11:59 PM"
        )

        def check_date_in_range_fun(date_str):
            date_obj = DeadlineUtils.datetime_str_to_datetime_obj(date_str)
            return datetime_start <= date_obj and date_obj <= datetime_end

        return check_date_in_range_fun

    # =======================================================
    # =======================================================

    @staticmethod
    def today_get_weekday():
        return datetime.today().isoweekday()

    # =======================================================
    # =======================================================

    @staticmethod
    def task_deadline_elapsed(deadline_str):
        deadline_obj = DeadlineUtils.datetime_str_to_datetime_obj(deadline_str)

        return deadline_obj < datetime.today()

    # =======================================================
    # =======================================================

    def recurring_task_new_deadline(deadline_str, frequency):

        today = datetime.today()

        n = int(frequency)
        deadline_obj = DeadlineUtils.datetime_str_to_datetime_obj(deadline_str)

        if today < deadline_obj:
            input("\nSomething Wrong. error occurred in recurring_task_new_deadline. ")
            return None

        while True:
            new_deadline = deadline_obj + timedelta(days=n)

            if new_deadline > today:
                deadline_csv = DeadlineUtils.datetime_obj_to_datetime_str(new_deadline)
                deadline = DeadlineUtils.datetime_str_to_deadline_column(deadline_csv)
                return deadline_csv, deadline
            else:
                deadline_obj = new_deadline

    # =======================================================
    # =======================================================


if __name__ == "__main__":

    from os_utils import OSUtils

    OS = OSUtils()
    OS.clear_screen()

    today = datetime.today()

    datetime_obj = today + timedelta(days=3)
    datetime_str = "01-01-2020 04:23 PM"

    datetime_list = [today + timedelta(days=i) for i in range(-5, 8)]
    datetime_str_list = [
        DeadlineUtils.datetime_obj_to_datetime_str(datetime_)
        for datetime_ in datetime_list
    ]

    print("datetime_obj_to_datetime_str:\n")
    datetime_str = DeadlineUtils.datetime_obj_to_datetime_str(datetime_obj)
    print(f"datetime_str : {datetime_str}")
    input("\npress enter to continue")

    print("datetime_str_to_datetime_obj:\n")
    datetime_obj = DeadlineUtils.datetime_str_to_datetime_obj(datetime_str)
    print(f"datetime_obj : {datetime_obj}")
    input("\npress enter to continue")

    print("datetime_str_to_deadline_column:\n")
    for datetime_str in datetime_str_list:
        print(
            datetime_str,
            "--",
            DeadlineUtils.datetime_str_to_deadline_column(datetime_str),
        )
    input("\npress enter to continue")

    print("deadline_csv_clean_up:\n")
    date_str, time_str = "02-03-2020  ", "8:02 am   "

    date_clean = DeadlineUtils.date_clean_up(date_str)
    time_clean = DeadlineUtils.time_clean_up(time_str)

    deadline_csv = DeadlineUtils.deadline_csv_clean_up(date_str, time_str)
    print(f"date_clean : {date_clean}")
    print(f"time_clean : {time_clean}")
    print(f"deadline_csv : {deadline_csv}")
    input("\npress enter to continue")

    print("check_date_in_range_fun_gen:\n")

    fun_1 = DeadlineUtils.check_date_in_range_fun_gen("01-01-2026", "20-01-2026")

    datetime_list = [datetime(2026, 1, 1) + timedelta(days=i * 5) for i in range(-3, 5)]
    datetime_str_list = [
        DeadlineUtils.datetime_obj_to_datetime_str(i) for i in datetime_list
    ]

    for date_str in datetime_str_list:
        print(date_str, "--", fun_1(date_str))
    input("\npress enter to continue")

    print("today_get_weekday:\n")
    print(DeadlineUtils.today_get_weekday())
    input("\npress enter to continue")
