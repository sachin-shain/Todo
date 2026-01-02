from config import input_format, invalid_choice
from storage import StorageManager
from task_manager import TaskManager
from cli_menus import CLI_menus


# Main Menu upon starting the program
def run(manager: TaskManager):
    while True:

        # print Main Menu
        CLI_menus.show_main_menu()

        # choose action
        choice = input_format("Enter your choice (1-5)", input_=True, new_line=True)

        if choice == "1":
            manager.add_tasks()
        elif choice == "2":
            manager.show_tasks()
        elif choice == "3":
            manager.update_tasks()
        elif choice == "4":
            manager.delete_tasks()
        elif choice == "5":
            manager.exit_main_menu()
            break
        else:
            invalid_choice()


def main():
    storage = StorageManager()
    manager = TaskManager(storage)
    run(manager)


if __name__ == "__main__":
    main()
