from .core import *

INSTALLED_APPS += depends.build('bases')

INSTALLED_APPS = list(set(INSTALLED_APPS))
