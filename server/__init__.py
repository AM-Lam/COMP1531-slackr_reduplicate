# pylint: disable=C0103

"""
sample code taken from:
https://stackoverflow.com/questions/1057431/how-to-load-all-modules-\
in-a-folder
added a few changes to exclude test files
"""

from os.path import dirname, basename, isfile, join
import glob


modules = glob.glob(join(dirname(__file__), "*.py"))

__all__ = [basename(f)[:-3] for f in modules if isfile(f)
           and not f.endswith('__init__.py') and not f.endswith("_test.py")]
