import pytest
from cron_parser.parser import BaseParser, CronParser


@pytest.fixture()
def default_parser():
    return BaseParser('*/15', 0, 59, 'minute')


@pytest.fixture()
def star_parser():
    return BaseParser('*', 1, 12, 'month')


@pytest.fixture()
def single_value_parser():
    return BaseParser('5', 1, 12, 'month')


@pytest.fixture()
def dash_parser():
    return BaseParser('10-15', 0, 23, 'hour')


@pytest.fixture()
def comma_parser():
    return BaseParser('1,16,27,54', 0, 59, 'minute')


@pytest.fixture()
def slash_parser():
    return BaseParser('*/10', 1, 31, 'day of month')


@pytest.fixture()
def slash_start_parser():
    return BaseParser('6/7', 1, 31, 'day of month')


@pytest.fixture()
def cron_parser():
    return CronParser('*/15 0 1,15 * 1-5 /usr/bin/find')


def test_parser_attributes(default_parser):
    assert default_parser.input == '*/15'


def test_parser_star_returns_all_elements(star_parser):
    assert star_parser.values == list(range(1, 13))


def test_parser_single_value_returns_single_element(single_value_parser):
    assert single_value_parser.values == [5]

def test_parser_dash_returns_values_in_range(dash_parser):
    assert dash_parser.values == [10, 11, 12, 13, 14, 15]


def test_parser_comma_returns_specific_values(comma_parser):
    assert comma_parser.values == [1, 16, 27, 54]


def test_parser_slash_star_returns_interval_values(slash_parser):
    assert slash_parser.values == [1, 11, 21, 31]


def test_parser_slash_starting_value_interval_values(slash_start_parser):
    assert slash_start_parser.values == [6, 13, 20, 27]


def test_parser_output(default_parser):
    assert default_parser.output == 'minute        0 15 30 45'


def test_parser_raises_value_error_on_invalid_input():
    error_parser = BaseParser('78', 0, 59, 'minute')
    with pytest.raises(ValueError):
        error_parser.values



def test_cron_parser_attributes(cron_parser):
    assert cron_parser.cron_string == '*/15 0 1,15 * 1-5 /usr/bin/find'
    assert isinstance(cron_parser.minute, BaseParser)
    assert isinstance(cron_parser.hour, BaseParser)
    assert isinstance(cron_parser.day_of_month, BaseParser)
    assert isinstance(cron_parser.month, BaseParser)
    assert isinstance(cron_parser.day_of_week, BaseParser)
    assert cron_parser.command == '/usr/bin/find'


def test_cron_parser_format_cron(cron_parser):
    expected_output = (
        'minute        0 15 30 45\n'
        'hour          0\n'
        'day of month  1 15\n'
        'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
        'day of week   1 2 3 4 5\n'
        'command       /usr/bin/find'
    )
    assert cron_parser.format_cron() == expected_output


def test_cron_parser_errors_when_six_elements_not_passed():
    with pytest.raises(ValueError):
        error_parser = CronParser('')
