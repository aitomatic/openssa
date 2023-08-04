# Helpful How-Tos

## Observability

`OpenSSM` has built-in observability and tracing.

## Logging

Users of `OpenSSM` can use the `logger` object provided by the `OpenSSM` package:

```python
from OpenSSM import logger
logger.warning("xyz = %s", xyz)
```

If you are an `OpenSSM` contributor, you may use the `openssm` logger:

```python
from openssm import mlogger
mlogger.warning("xyz = %s", xyz)
```

### Automatic function logging

There are some useful decorators for automatically logging function entry and exit.

```python
from openssm import Logs

@Logs.do_log_entry_and_exit()  # upon both entry and exit
def func(param1, param2):

@Logs.do_log_entry()  # only upon entry

@Logs.do_log_exit()   # only upon exit
```

The above will automatically log function entry with its parameters, and function exit with its return value.

If you want to use your own logger with its own name, use

```python
from openssm import Logs
my_logger = Logs.get_logger(app_name, logger.INFO)

@Logs.do_log_entry_and_exit(logger=my_logger)
def func(param1, param2):
```

Sometimes it is useful to be able to specify additional parameters to be logged:

```python
@Logs.do_log_entry_and_exit({'request': request})
```
