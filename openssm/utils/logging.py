import logging
import functools


logger: logging.Logger = None


class Logging:
    _logger = None

    @staticmethod
    def str_to_log_level(level_str='WARNING'):
        level_str = level_str.upper()
        return getattr(logging, level_str, logging.WARNING)

    @staticmethod
    def _add_handler_to(a_logger: logging.Logger):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
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
        handler.setFormatter(formatter)

        # add the handlers to logger
        # pylint: disable=protected-access
        a_logger.addHandler(handler)
        a_logger.propagate = False

    @staticmethod
    def get_logger(name=None, log_level=logging.DEBUG) -> logging.Logger:
        a_logger = logging.getLogger(name)
        a_logger.setLevel(log_level)
        Logging._add_handler_to(a_logger)
        return a_logger

    @staticmethod
    def _get_top_package_name():
        top_package = __name__.split('.', maxsplit=1)[0]
        return top_package

    @staticmethod
    def get_package_logger(log_level=logging.WARNING):
        a_logger = Logging.get_logger(name=Logging._get_top_package_name(), log_level=log_level)
        Logging._logger = a_logger
        return a_logger

    @staticmethod
    def do_log_entry_and_exit(*extra_args, the_logger=None, log_level=logging.DEBUG, log_entry=True, log_exit=True):
        """
        Decorator to log function entry and exit.
        """
        if the_logger is None:
            the_logger = Logging._logger

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
        return Logging.do_log_entry_and_exit(extra_args, log_level=log_level, log_entry=True, log_exit=False)

    @staticmethod
    def do_log_exit(*extra_args, log_level=logging.DEBUG):
        """
        Decorator to log function exit.
        """
        return Logging.do_log_entry_and_exit(extra_args, log_level=log_level, log_entry=False, log_exit=True)


logger = Logging.get_package_logger(logging.WARN)
"""A global logger for the package"""
