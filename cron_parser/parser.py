import argparse


class BaseParser:

    def __init__(self, value, start, end, parser_type):
        self._input = value
        self._start = start
        self._end = end
        self._parser_type = parser_type

    @property
    def input(self):
        return self._input

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def parser_type(self):
        return self._parser_type

    @property
    def _all_values(self):
        return list(range(self.start, self.end + 1))

    @property
    def output(self):
        """Returns parser type (14 character padding) and values"""
        string_values = ' '.join([str(x) for x in self.values])
        return f"{self.parser_type:14}{string_values}"

    def range_values(self):
        """Returns all values within and including the given range."""
        start, end = [int(x) for x in self.input.split('-')]
        return [x for x in self._all_values if start <= x <= end]

    def specific_values(self):
        """Returns each value for the given comma separated list."""
        values = [int(x) for x in self.input.split(',')]
        return values

    def interval_values(self):
        """
            Returns all values for the given interval and starting point.
            e.g 2/3 would return 2 5 8 11 etc
        """
        start, interval = self.input.split('/')
        # determine the index starting point for intervals
        index = 0 if start == '*' else self._all_values.index(int(start))
        return self._all_values[index::int(interval)]

    @property
    def values(self):
        try:
            if self.input == '*':
                return self._all_values
            elif '-' in self.input:
                return self.range_values()
            elif ',' in self.input:
                return self.specific_values()
            elif '/' in self.input:
                return self.interval_values()
            elif int(self.input) in self._all_values:
                return [int(self.input)]
            # Yeah I don't like this, but just wanted to error out if
            # all else failed
            else:
                raise ValueError()
        except:
            raise ValueError(f'Unable to parse the {self.parser_type} element')


class CronParser:

    def __init__(self, cron_string):
        self._cron_string = cron_string
        self.parse_string()

    @property
    def cron_string(self):
        return self._cron_string

    def parse_string(self):
        elements = self.cron_string.split()
        if len(elements) != 6:
            raise ValueError(
                f'There are unexpected elements. Expected 6 but got {len(elements)}'
            )
        self.minute = BaseParser(elements[0], 0, 59, 'minute')
        self.hour = BaseParser(elements[1], 0, 23, 'hour')
        self.day_of_month = BaseParser(elements[2], 1, 31, 'day of month')
        self.month = BaseParser(elements[3], 1, 12, 'month')
        self.day_of_week = BaseParser(elements[4], 1, 7, 'day of week')
        self.command = elements[5]

    def format_cron(self):
        return (
            f"{self.minute.output}\n"
            f"{self.hour.output}\n"
            f"{self.day_of_month.output}\n"
            f"{self.month.output}\n"
            f"{self.day_of_week.output}\n"
            f"{'command':14}{self.command}"
        )


if __name__ == '__main__':
    args_parse = argparse.ArgumentParser()
    args_parse.add_argument('cron_string')
    args = args_parse.parse_args()

    cron_parse = CronParser(**vars(args))
    print(cron_parse.format_cron())
