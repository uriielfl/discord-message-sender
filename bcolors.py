class BashColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    NORMAL = "\033[97m"
    WARNING = "\033[33m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def colored_print(
    text: str = "",
    color: BashColors = None,
    start_spaces: int = 0,
    end_spaces: int = 0,
    separator: bool = False,
):
    if start_spaces:
        for space in range(0, start_spaces):
            print("\n")
    print(f"{color}{text}{BashColors.RESET}")
    if start_spaces:
        for space in range(0, end_spaces):
            print("\n")
    if separator:
        print("===========================================")
