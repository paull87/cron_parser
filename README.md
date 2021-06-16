# Cron Parser

### Overview
This commpand line script parses a cron string and expands each field
to show the times at which it will run. It considers the standard cron format 
with five time fields (minute, hour, day of month, month, and day of week) plus a command.
The output will be a table format with the field name taking the first 14 columns and
the times as a space-separated list following it, e.g. 

```
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```

### Setup

This is run using python 3.7 and includes `requirements.txt` for dependent libraries.


### Usage

The program can be run by using the following command

```python
python -m cron_parser.parser "0 1-3 7/7 3/3 1/2 /usr/bin/find"
```

This will output a standardised cron format to the console, i.e.

```
minute        0
hour          1 2 3
day of month  7 14 21 28
month         3 6 9 12
day of week   1 3 5 7
command       /usr/bin/find
```


### Tests

There are a number of unit tests in `cron_parser/tests` that cover the functionality
of the cron parser. These have been created using pytest and can be run using `pytest tests`