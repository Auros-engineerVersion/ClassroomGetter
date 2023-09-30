import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from pathlib import Path
from shutil import rmtree
from unittest.mock import MagicMock, patch

from src.data import *
from src.my_util import arrow
from src.settings import *


class SettingTest(unittest.TestCase):
    def test_invailed_path(self):
        self.assertRaises(FileNotFoundError, save, Path('.'), SettingData())
        self.assertRaises(FileNotFoundError, load, Path('.'))