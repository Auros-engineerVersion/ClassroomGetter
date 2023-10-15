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
        self.recode0 = MinimalistRecode(value=0)
        self.recode1 = MinimalistRecode(value=1)
        self.recode2 = MinimalistRecode(value=2)
        self.id0 = self.db.add(self.recode0)
        self.id1 = self.db.add(self.recode1)
        self.id2 = self.db.add(self.recode2)
        
    def tearDown(self) -> None:
        del self.db

    def test_add(self):
        recode3 = MinimalistRecode(value=30)
        id3 = self.db.add(recode3)
        self.assertEqual(id3, 3)
        self.assertEqual(len(self.db), 4)
        
    def test_add_with_unique(self):
        before_len = len(self.db)
        
        same_value_recode = MinimalistRecode(value=10)
        id = self.db.add_with_unique(same_value_recode)
        self.assertEqual(id, self.id1)
        self.assertEqual(len(self.db), before_len)

    def test_get_fromID(self):
        self.assertEqual(self.db.get_fromID(self.id0), self.recode0)
        self.assertEqual(self.db.get_fromID(self.id1), self.recode1)
        self.assertEqual(self.db.get_fromID(self.id2), self.recode2)
        
        self.db.remove(self.id1)
        self.assertIsNone(self.db.get_fromID(self.id1))
        self.assertEqual(self.db.get_fromID(self.id2), self.recode2)
        
    def test_remove(self):
        self.assertRaises(TypeError, self.db.remove, 100)
        
        self.assertEqual(len(self.db), 3)
        self.db.remove(self.id0)
        self.assertEqual(len(self.db), 2)
        
        self.db.remove(self.id1)
        self.db.remove(self.id2)
        self.assertEqual(len(self.db), 0)