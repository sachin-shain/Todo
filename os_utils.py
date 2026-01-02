import os


class OSUtils:
    """Handles OS utilities

    variables:
        cwd

    functions:
        @staticmethod
            clear_screen()
            cwd() -> str
        check_file_exists(file_name)
        make_hidden(file_name)
        make_unhidden(file_name)
        get_pdf_path(pdf_path: str = "") -> str
    """

    # clear screen. nt ==> new technology (windows),
    #               clear ==> linux, mac, etc.
    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")
        # print("\n\n")
        # print("==" * 50)
        # print("\n\n")

    # current working directory: ~\...\ToDo\
    @staticmethod
    def cwd():
        path = os.getcwd()
        path = path.replace("\\", "/")
        return path + "/"

    def __init__(self):
        # current working directory
        self.cwd = OSUtils.cwd()

    # check if the file exists. return True if it does
    def check_file_exists(self, file_name):
        file_path = self.cwd + file_name
        return os.path.isfile(file_path)

    # to make file hidden
    def make_hidden(self, file_name):
        file_path = self.cwd + file_name
        cmd = f"attrib +h {file_path}"
        os.system(cmd)

    # to make file unhidden
    def make_unhidden(self, file_name):
        file_path = self.cwd + file_name
        cmd = f"attrib -s -h {file_path}"
        os.system(cmd)

    # desktop path
    def get_pdf_path(self, pdf_path: str = ""):
        if pdf_path == "":
            pdf_path = os.path.join(os.path.expanduser("~"), "Desktop")
            pdf_path = pdf_path.replace("\\", "/")

        return pdf_path + "/"


if __name__ == "__main__":

    OS = OSUtils()
    OS.clear_screen()

    print("Entering cwd:\n")
    print(OSUtils.cwd())
    print("Exiting cwd\n")

    print("Entering cwd:\n")
    file_name = "tasks.csv"
    print(OS.check_file_exists(file_name))
    print("Exiting cwd\n")

    print("Entering cwd:\n")
    pdf_path = ""
    print(OS.get_pdf_path(pdf_path))

    pdf_path = OSUtils.cwd()[:-1]
    print(OS.get_pdf_path(pdf_path))
    print("Exiting cwd\n")
