# flake8: noqa

import logging
import sys
from qtpy import QT_VERSION

__appname__ = "岩石薄片智能识别系统"
__version__ = "4.5.7"

QT4 = QT_VERSION[0] == "4"
QT5 = QT_VERSION[0] == "5"
del QT_VERSION

PY2 = sys.version[0] == "2"
PY3 = sys.version[0] == "3"
del sys


