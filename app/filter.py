import babel


def format_datetime(value, format='yy/MM/dd'):
    return babel.dates.format_datetime(value, format)

def format_gdatetime(value, format='yyyy-MM-dd'):
    return babel.dates.format_datetime(value, format)


def number_format_simple(value):
    return '{:,}'.format(value)
