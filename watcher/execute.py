__author__ = 'david_allison'

from subprocess import call
call(["ls", "-l"])
call(["finger"])
call(["ping", "-c", "10", "localhost"])