import csv

from io import StringIO, BytesIO

import sys

from pkg_resources import resource_string


def get_csv(file_name):
    contents = resource_string('pogoiv', 'data/%s' % file_name)

    if sys.version_info >= (3, 0):
        f = StringIO(contents.decode('utf-8'))
    else:
        f = BytesIO(contents)

    return csv.reader(f, delimiter='\t')
