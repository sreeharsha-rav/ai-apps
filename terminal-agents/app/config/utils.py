class CustomLogger:
    """
    A simple wrapper around print to provide styled logging without conflicting with rich.Live.
    """
    def debug(self, message: str):
        # Dim Cyan
        print(f"\033[2;36mDEBUG:\033[0m {message}")

    def info(self, message: str):
        # Bold Blue
        print(f"\033[1;34mINFO:\033[0m {message}")

    def warning(self, message: str):
        # Bold Yellow
        print(f"\033[1;33mWARNING:\033[0m {message}")

    def error(self, message: str):
        # Bold Red
        print(f"\033[1;31mERROR:\033[0m {message}")

logger = CustomLogger()
