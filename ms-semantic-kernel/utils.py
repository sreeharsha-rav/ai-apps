class CustomLogger:
    """A custom logger class with colorized print output by log level."""

    COLORS = {
        "DEBUG": "\033[94m",    # Blue
        "INFO": "\033[92m",     # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",    # Red
        "CRITICAL": "\033[95m", # Magenta
        "RESET": "\033[0m",
    }

    def log(self, message: str, level: str = "INFO") -> None:
        """Print a colorized log message."""
        level = level.upper()
        color = self.COLORS.get(level, self.COLORS["INFO"])
        reset = self.COLORS["RESET"]
        print(f"{color}[{level}] {message}{reset}")

    def debug(self, message: str) -> None:
        self.log(message, "DEBUG")

    def info(self, message: str) -> None:
        self.log(message, "INFO")

    def warning(self, message: str) -> None:
        self.log(message, "WARNING")

    def error(self, message: str) -> None:
        self.log(message, "ERROR")

    def critical(self, message: str) -> None:
        self.log(message, "CRITICAL")

    