# TO-DO: Manage tasks

Provides a platform to manage tasks and improve time management using Eisenhower Matrix.

The tasks are saved in *to_do.csv* file.

## Task features

* Priority:

    | Priority | Urgency/importance   |
    |---|---|
    | Do it now! | urgent/important   |
    | Decide when to do it.  | not-urgent/important   |  
    | Delegate!  | urgent/not-important   |
    | Do it later/dump it!| not-urgent/not-important   |

* Task description
* Sub tasks
  * Sub task description: If there are no sub tasks, it is denoted as '\---'.
  * Deadline: If the deadline is passed, the task is upgraded to 'Do it now!' priority and marked as overdue.
    | Deadline format | Deadline category|
    | ---|---|
    | Overdue: 4 days ago <br>  Overdue: Today  04:25 AM | Overdue |
    | Overdue: Today  04:25 AM <br> Today  11:59 AM| tasks due today|
    | Overdue: Today  04:25 AM <br> Today  11:59 AM <br> Thursday 2:00 PM <br> Sunday 3:00 PM | tasks due by this weekend|
    | 24-09-2024 10:13 PM | Due after the weekend|
  * Status : Not started, In progress, Completed
  * Comment
    | Comment format | Comment category|
    | --- | --- |
    | \---| No comment|
    | Schedule: *text* |  priority : Decide when to do it|
    |delegate to *text*| priority : Delegate|
    | do it later <br> dump it | priority: Do it later/dump it|

## Main menu

* Add tasks
* Update tasks : status, deadline, and comment.
* Print tasks
  * All
  * Priority
  * Status
  * Deadline : Overdue, Today, This week, date range
* Delete tasks : Completed, task ID, sub task ID
* Quit
