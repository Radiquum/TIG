import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")
# log.info("Hello, World! 123", extra={"markup": True, "style": "bold cyan", "highlighter": None})
# log.warning("Hello, WARN 123!", extra={"markup": True, "style": "bold cyan", "highlighter": None})
# log.error("Hello, World! 123", extra={"markup": True, "style": "bold cyan", "highlighter": None})