import os
import logging
import functools


# logger is an application-level logger that can be used anywhere in user code
logger: logging.Logger = None

# mlogger is a library-level logger that can be used anywhere in openssa code
mlogger: logging.Logger = None


class Logs:
    # Use a unique signature to identify my handler
    _MY_HANDLER_SIGNATURE = 'di93mwl#'

    @staticmethod
    def _str_to_log_level(level_str='WARNING'):
        level_str = level_str.upper()
        return getattr(logging, level_str, logging.WARNING)

    @staticmethod
    def _new_handler() -> logging.Handler:
        """
        Creates a new handler with the default format.
        Here is where we can change the Observable platform
        to output the logs to.
        """
        new_handler = logging.StreamHandler()
        new_handler.setLevel(logging.DEBUG)

        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        # formatter = logging.Formatter(
        #    '%(asctime)s [%(levelname)s]: %(module)s.%(funcName)s (in %(filename)s line %(lineno)d) %(message)s',
        #    datefmt='%m/%d/%Y %I:%M:%S %p'
        # )
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s]: %(name)s.%(module)s.%(funcName)s (in %(filename)s line %(lineno)d) %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )
        new_handler.setFormatter(formatter)
        return new_handler

    @staticmethod
    def get_logger(name=None, log_level=logging.DEBUG) -> logging.Logger:
        """Gets a new/existing logger with the given name and log level"""
        new_logger = logging.getLogger(name)
        new_logger.setLevel(log_level)

        for handler in new_logger.handlers:
            if handler.get_name() == Logs._MY_HANDLER_SIGNATURE:
                # The logger already has a handler with my signature
                return new_logger

        # Add convenience constants so the user doesn't have to import logging
        new_logger.DEBUG = logging.DEBUG
        new_logger.INFO = logging.INFO
        new_logger.WARNING = logging.WARNING
        new_logger.ERROR = logging.ERROR
        new_logger.CRITICAL = logging.CRITICAL

        new_handler = Logs._new_handler()
        new_handler.set_name(Logs._MY_HANDLER_SIGNATURE)
        new_logger.addHandler(new_handler)

        # new_logger.propagate = False

        return new_logger

    @staticmethod
    def _get_top_package_name():
        return __name__.split('.', maxsplit=1)[0]

    @staticmethod
    def do_log_entry_and_exit(*extra_args, the_logger=None, log_level=logging.DEBUG, log_entry=True, log_exit=True):
        """
        Decorator to log function entry and exit.
        """
        the_logger = the_logger or mlogger

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):

                if log_entry:
                    arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
                    args_list = tuple(f"{name}={arg}" for name, arg in zip(arg_names, args)) + tuple(f"{k}={v}" for k, v in kwargs.items())

                    # Log extra arguments
                    for extra_arg in extra_args:
                        if isinstance(extra_arg, dict):
                            args_list += tuple(f"{k}={v}" for k, v in extra_arg.items())
                        else:
                            args_list += (f"extra_arg={extra_arg}",)

                    the_logger.log(log_level, "Calling %s with args: %s", func.__name__, args_list)

                result = func(*args, **kwargs)

                if log_exit:
                    the_logger.log(log_level, "Function %s returned: %s", func.__name__, result)

                return result
            return wrapper
        return decorator

    @staticmethod
    def do_log_entry(*extra_args, log_level=logging.DEBUG):
        """
        Decorator to log function entry.
        """
        return Logs.do_log_entry_and_exit(extra_args, log_level=log_level, log_entry=True, log_exit=False)

    @staticmethod
    def do_log_exit(*extra_args, log_level=logging.DEBUG):
        """
        Decorator to log function exit.
        """
        return Logs.do_log_entry_and_exit(extra_args, log_level=log_level, log_entry=False, log_exit=True)


logger = Logs.get_logger(os.path.basename(os.getcwd()), logging.DEBUG)

# pylint: disable=protected-access
mlogger = Logs.get_logger(Logs._get_top_package_name(), logging.WARN)
