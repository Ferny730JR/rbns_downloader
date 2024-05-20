import sys
import logging

# ANSI color codes
ANSI_COLOR_RED = "\x1b[31m"
ANSI_COLOR_GREEN = "\x1b[32m"
ANSI_COLOR_YELLOW = "\x1b[33m"
ANSI_COLOR_BLUE = "\x1b[34m"
ANSI_COLOR_MAGENTA = "\x1b[35m"
ANSI_COLOR_CYAN = "\x1b[36m"
ANSI_COLOR_BRIGHT = "\x1b[1m"
ANSI_COLOR_RESET = "\x1b[0m"

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logging.getLogger().handlers.clear()

# Output in color, with specified format
class ColorFormatter(logging.Formatter):
	def format(self, record):
		message = super().format(record)
		if record.levelno == logging.ERROR:
			return f"{ANSI_COLOR_RED}ERROR: {ANSI_COLOR_RESET}{ANSI_COLOR_BRIGHT}{message}{ANSI_COLOR_RESET}"
		elif record.levelno == logging.WARNING:
			return f"{ANSI_COLOR_RED}WARNING: {ANSI_COLOR_RESET}{ANSI_COLOR_BRIGHT}{message}{ANSI_COLOR_RESET}"
		return message

# Update stream handler specifications
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(ColorFormatter())
logger = logging.getLogger()
logger.addHandler(handler)
logger.propagate = False


def error_message(format_string, *args):
	"""Print an error message to stderr

	Args:
		format_string (str): F-String to output to stderr as an error
	"""
	logger.error(format_string % args)

def warning_message(format_string, *args):
	"""Print a warning message to stderr

	Args:
		format_string (str): F-String to output to stderr as a warning
	"""
	logger.warning(format_string % args)

def remove_lines(n: int) -> None:
	"""Remove `n` number of lines from the command line interface

	Args:
		`n` (int): Number of lines to remove
	"""
	for _ in range(n):
		sys.stdout.write("\033[F")  # Move cursor up one line
		sys.stdout.write("\033[K")  # Clear the line

def remove_line() -> None:
	sys.stdout.write("\033[K")

# Example usage:
if __name__ == "__main__":
	error_message("This is an %s message with code %d", "error", 404)
	warning_message("This is a %s message with code %d", "warning", 301)
