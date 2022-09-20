import unittest
import numpy as np
import math

class ElseOther(unittest.TestCase):

    def test_attribute(self, color='red'):
        self.color = color
        self.assertEqual(self.color, 'red')
        
    def test_cast(self):
        self.assertEqual(3, int('3'))

    def test_nan(self):
        a = np.nan
        self.assertTrue(math.isnan(a))
        #self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)