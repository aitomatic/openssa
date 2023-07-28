# Helpful How-Tos

## Observability

`OpenSSM` has built-in observability and tracing.

## Logging

Users of `OpenSSM` should create their own loggers:
```python
import logging
from OpenSSM import Logging
logger = Logging.get_logger(app_name, logging.INFO)
logger.warn("xyz = %s", xyz)
```

If you are an `OpenSSM` contributor, you may use the default logger:

```python
from openssm import logger
logger.warn("xyz = %s", xyz)
```

### Automatic function logging

There are some useful decorators for automatically logging function entry and exit.

```python
from openssm import Logging

@Logging.do_log_entry_and_exit  # upon both entry and exit
def func(param1, param2):

@Logging.do_log_entry  # only upon entry

@Logging.do_log_exit   # only upon exit
```

The above will automatically log function entry with its parameters, and function exit with its return value.

If you want to use your own logger with its own name, use
```python
from openssm import Logging, logger
logger = Logging.get_logger(app_name, logging.INFO)

@Logging.do_log_entry_and_exit(logger=logger)
def func(param1, param2):
```

Sometimes it is useful to be able to specify additional parameters to be logged:

```python
@Logging.do_log_entry_and_exit({'request': request})
```
