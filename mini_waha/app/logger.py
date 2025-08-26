from pathlib import Path
from loguru import logger


def setup_logging() -> None:
    """Configure loguru logging to file and stdout."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger.remove()
    logger.add(log_dir / "app.log", rotation="1 day", serialize=False)
    logger.add(lambda msg: print(msg, end=""))


setup_logging()
