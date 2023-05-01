# HERE STARTS DYNACONF EXTENSION LOAD (Keep at the very bottom of settings.py)
# Read more at https://www.dynaconf.com/django/
from inspect import getsourcefile
from pathlib import Path

from django.urls import reverse_lazy

import dynaconf
from dynaconf.utils import parse_conf

parse_conf.converters["@reverse_lazy"] = lambda value: parse_conf.Lazy(value, casting=reverse_lazy)

settings = dynaconf.DjangoDynaconf(
    __name__,
    # Take the absolute, resolved file path and traverse up 3 levels to get the root path
    root_path=Path(getsourcefile(lambda: 0)).resolve().parent.parent.parent,
)
# HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)
