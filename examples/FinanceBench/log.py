from pathlib import Path
import sys

from loguru import logger


LOG_DIR_PATH: Path = Path(__file__).parent / '.log'
CURRENT_LOG_HANDLER_ID: int | None = None


# loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add
logger.add(sink=sys.stdout, level='DEBUG',
           # format=...,
           filter=None,
           colorize=True,
           serialize=False,
           backtrace=True, diagnose=True,
           enqueue=False, context=None,
           catch=True)


def switch_log_file(name: str, /):
    global CURRENT_LOG_HANDLER_ID  # pylint: disable=global-statement

    if CURRENT_LOG_HANDLER_ID is not None:
        logger.remove(handler_id=CURRENT_LOG_HANDLER_ID)

    CURRENT_LOG_HANDLER_ID = logger.add(sink=Path(LOG_DIR_PATH) / f'{name}.log', level='DEBUG',
                                        # format=...,
                                        filter=None,
                                        colorize=True,
                                        serialize=False,
                                        backtrace=True, diagnose=True,
                                        enqueue=False, context=None,
                                        catch=True)
