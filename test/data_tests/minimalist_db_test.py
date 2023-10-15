import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest

from src.data.minimalist_db import *


class MinimalistRecodeTest(unittest.TestCase):
    def test_eq(self):
        zero = MinimalistRecode(value=0)
        self.assertEqual(zero, zero)
        
        one = MinimalistRecode(value=1)
        self.assertNotEqual(zero, one)
        
        self.assertEqual(zero, 0)
        self.assertNotEqual(one, 0)

class MinimalistDBTest(unittest.TestCase):
    def setUp(self):
        self.db = MinimalistDB()
        self.recode0 = MinimalistRecode(value=00)
        self.recode1 = MinimalistRecode(value=10)
        self.recode2 = MinimalistRecode(value=20)
        self.id0 = self.db.add(self.recode0)
        self.id1 = self.db.add(self.recode1)
        self.id2 = self.db.add(self.recode2)
        
    def tearDown(self) -> None:
        del self.db

    def test_add(self):
        recode3 = MinimalistRecode(value=30)
        id3 = self.db.add(recode3)
        self.assertEqual(id3, 3)
        self.assertEqual(self.db.get(id3), recode3)

    def test_get(self):
        self.assertEqual(self.db.get(self.id0), self.recode0)
        self.assertEqual(self.db.get(self.id1), self.recode1)
        self.assertEqual(self.db.get(self.id2), self.recode2)

    def test_remove(self):
        self.db.remove(self.id1)
        self.assertIsInstance(self.db.get(self.id1), EmptyRecode)
        self.assertEqual(len(self.db) , 2)

    def test_remove_target(self):
        self.db.remove_target(self.recode1)
        self.assertIsInstance(self.db.get(self.id1), EmptyRecode)
        
    def test_min(self):
        self.assertEqual(min(self.db), self.recode0)