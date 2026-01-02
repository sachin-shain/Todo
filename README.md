# TO-DO: Manage tasks

Provides a platform to manage tasks and improve time management using Eisenhower Matrix.

The tasks are saved in *tasks.csv* file.

## Task features

* Priority:

    | Priority              | Urgency/importance       |
    | --------------------- | ------------------------ |
    | Do it now!            | urgent/important         |
    | Decide when to do it. | not-urgent/important     |
    | Delegate!             | urgent/not-important     |
    | Do it later/dump it!  | not-urgent/not-important |

* Task description
* Sub tasks
  * Sub task description: If there are no sub tasks, it is denoted as '\---'.
  * Deadline: If the deadline is passed, the task is upgraded to 'Do it now!' priority and marked as overdue.
  * If an 'overdue' task is marked 'Completed', 'overdue' prefix is removed
    | Deadline format                                                                         | Deadline category         |
    | --------------------------------------------------------------------------------------- | ------------------------- |
    | Overdue: 4 days ago <br>  Overdue: Today  04:25 AM ,<br> Overdue: Yesterday 11:59 PM    | Overdue                   |
    | Overdue: Today  04:25 AM <br> Today  11:59 AM                                           | tasks due today           |
    | Overdue: Today  04:25 AM <br> Today  11:59 AM <br> Thursday 2:00 PM <br> Sunday 3:00 PM | tasks due by this weekend |
    | 24-09-2024 10:13 PM                                                                     | Due after the weekend     |
  * Status : Not started, In progress, Completed
  * Comment
    | Comment format           | Comment category                |
    | ------------------------ | ------------------------------- |
    | \---                     | No comment                      |
    | Schedule: *text*         | priority : Decide when to do it |
    | delegate to *text*       | priority : Delegate             |
    | do it later <br> dump it | priority: Do it later/dump it   |
* If the task are recurring, mark them as recurring with recurring frequency
  * If recurring task's deadline elapsed, the deadline will get updated to next recurring date
* Generate pdfs of all tasks, overdue tasks, tasks due today, and tasks due this weekend.
  * The folder in which these pdfs are generated at give at *config.py/PDF_PATH* 
## Main menu

* Add tasks
* Update tasks : status, deadline, and comment.
* Print tasks
  * All
  * Priority
  * Status
  * Deadline : Overdue, Today, This week, date range
  * Recurring tasks
* Delete tasks : Completed, task ID or sub task ID
* Quit
## Running the package
* Required python packages are listed in *requirements.txt*
  * numpy
  * pandas
  * reportlab
* Creating a new Conda environment 
  ```bash
  conda create -n todo_env
  conda activate todo_env
  pip install -r requirements.txt
  ```
* Running the package
  ```bash
  python main.py
  ```
* Get generate sample tasks
  ```bash
  python test_task_gen.py
  ```
  * To remove the sample data, delete all .pdf and .csv files