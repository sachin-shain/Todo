from config import *
from deadlines import DeadlineUtils as DU
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
import random


task_no = 20


def random_gen(start=0, end=task_no, n=1):
    return [random.randint(start, end - 1) for _ in range(n)]


file_name = "tasks.csv"
task_with_subtask_num = 10


task_with_subtask_indices = random_gen(n=task_with_subtask_num)

df = pd.DataFrame(columns=TASK_COLUMNS)

for i in range(1, task_no):
    priority = PRIORITY_CATEGORIES[random.sample(range(4), 1)[0]]
    task = f"task_{i}"
    if not i in task_with_subtask_indices:

        sub_task = "---"
        status = STATUS_CATEGORIES[random.sample(range(3), 1)[0]]
        comment = f"comment_{i}"
        deadline_csv = "---"
        deadline = "---"

        data = [priority, task, sub_task, status, comment, deadline_csv, deadline]
        df.loc[len(df)] = data
    else:
        for j in range(random.sample(range(2, 5), 1)[0]):
            sub_task = f"sub_task_{i}_{j}"
            status = STATUS_CATEGORIES[random.sample(range(3), 1)[0]]
            comment = f"comment_{i}_{j}"
            deadline_csv = "---"
            deadline = "---"

            data = [priority, task, sub_task, status, comment, deadline_csv, deadline]
            df.loc[len(df)] = data
df_len = len(df)

comment_is_nan_index_list = random_gen(0, df_len, 8)

for idx in comment_is_nan_index_list:
    df.loc[idx, "Comment"] = "---"

deadline_list = []

today = datetime.today()
today_date = today.date()

deadline_list.append(today)
deadline_list.append(today + timedelta(minutes=5))
deadline_list.append(today + timedelta(minutes=-5))
deadline_list.append(today + timedelta(minutes=10))
deadline_list.append(today + timedelta(minutes=-10))
d = (today + timedelta(days=-1)).date()
deadline_list.append(datetime.combine(d, time(23, 59)))
d = today.date()
deadline_list.append(datetime.combine(d, time(23, 59)))

no_of_dates_left = df_len - 7
no_of_dates_before = no_of_dates_left // 3
no_of_dates_after = no_of_dates_left - no_of_dates_before

for i in range(1, no_of_dates_before + 1):
    deadline_list.append(today + timedelta(days=-i))

for i in range(1, no_of_dates_after + 1):
    deadline_list.append(today + timedelta(days=i))
deadline_list.sort()
for idx, datetime_ in enumerate(deadline_list):
    datetime_str = DU.datetime_obj_to_datetime_str(datetime_)
    deadline = DU.datetime_str_to_deadline_column(datetime_str)

    df.loc[idx, "Deadline_csv"] = datetime_str
    df.loc[idx, "Deadline"] = deadline


df.to_csv(file_name, index=False)

# =======================================================
# =======================================================

file_name = RECURRING_FILENAME

recurring_tasks_num = task_no // 5

task_list = df["Tasks"].unique()

rec_tasks_idx_list = list(random_gen(0, len(task_list), recurring_tasks_num))

rec_tasks_idx_list.sort()

recurring_tasks_list = [task_list[i] for i in rec_tasks_idx_list]

r_df = pd.DataFrame(columns=RECURRING_TASK_COLUMNS)

for task in recurring_tasks_list:
    r_df.loc[len(r_df)] = [task, random_gen(1, 8)[0]]

r_df.to_csv(file_name, index=False)
