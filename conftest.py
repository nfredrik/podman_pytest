import pytest
import logging

class ColorFormatter(logging.Formatter):
    # Define ANSI escape sequences for colors.
    COLORS = {
        'DEBUG': "\033[37m",     # White
        'INFO': "\033[32m",      # Green
        'WARNING': "\033[33m",   # Yellow
        'ERROR': "\033[31m",     # Red
        'CRITICAL': "\033[41m",  # Red background
    }
    RESET_SEQ = "\033[0m"

    def format(self, record):
        # Get the original formatted message.
        original_message = super().format(record)
        # Determine the color based on the record's level.
        color = self.COLORS.get(record.levelname, self.RESET_SEQ)
        # Add the color sequences to the message.
        return f"{color}{original_message}{self.RESET_SEQ}"

@pytest.fixture
def log():
    logger = logging.getLogger("coloredLogger")
    logger.setLevel(logging.DEBUG)

    # Create a stream handler (prints to stdout).
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # Create and set the custom formatter.
    formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger.
    logger.addHandler(stream_handler)

    return logger, 'hej'



def pytest_addoption(parser):
    parser.addoption(
        "--myarg",
        action="store",
        default="default_value",
        help="A simple custom argument for tests"
    )


@pytest.fixture
def myarg(request):
    return request.config.getoption("--myarg")