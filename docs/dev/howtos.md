# Helpful How-Tos

## Observability

`OpenSSA` has built-in observability and tracing.

## Logging

Users of `OpenSSA` can use the `logger` object provided by the `OpenSSA` package:

```python
from OpenSSA import logger
logger.warning("xyz = %s", xyz)
```

If you are an `OpenSSA` contributor, you may use the `OpenSSA` logger:

```python
from OpenSSA import mlogger
mlogger.warning("xyz = %s", xyz)
```

### Automatic function logging

There are some useful decorators for automatically logging function entry and exit.

```python
from OpenSSA import Logs

@Logs.do_log_entry_and_exit()  # upon both entry and exit
def func(param1, param2):

@Logs.do_log_entry()  # only upon entry

@Logs.do_log_exit()   # only upon exit
```

The above will automatically log function entry with its parameters, and function exit with its return value.

If you want to use your own logger with its own name, use

```python
from OpenSSA import Logs
my_logger = Logs.get_logger(app_name, logger.INFO)

@Logs.do_log_entry_and_exit(logger=my_logger)
def func(param1, param2):
```

Sometimes it is useful to be able to specify additional parameters to be logged:

```python
@Logs.do_log_entry_and_exit({'request': request})
```
