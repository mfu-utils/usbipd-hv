import os
import sys
from os.path import abspath, dirname

ROOT = dirname(abspath(__file__))
CWD = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else ROOT

INI_FILE_PATH = os.path.join(CWD, "config.ini")
