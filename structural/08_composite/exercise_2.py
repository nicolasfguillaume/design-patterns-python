# Composite Coding Exercise

# Consider the code presented below. We have two classes called SingleValue and ManyValues. SingleValue stores 
# just one numeric value, but ManyValues can store either numeric values or SingleValue objects.

# You are asked to give both SingleValue and ManyValues a property member called sum that returns 
# a sum of all the values that the object contains. Please ensure that there is only a single method 
# that realizes the property sum, not multiple methods.

import unittest
from abc import ABC
from collections.abc import Iterable


# ValueContainer is an abstract, iterable base class, which enforces that subclasses must implement the __iter__() method
class ValueContainer(Iterable, ABC):
    @property
    def sum(self):
        result = 0
        for item in self:
            if isinstance(item, int):
                result += item
            else:
                for i in item:
                    result += i
        return result


class SingleValue(ValueContainer):
    def __init__(self, value):
        self.value = value

    # convert a scalar value into a collection of 1 element (i.e. an iterable)
    def __iter__(self):
        yield self.value


class ManyValues(list, ValueContainer):
    pass


class FirstTestSuite(unittest.TestCase):
    def test_single_values(self):
        single_value = SingleValue(11)
        self.assertEqual(single_value.sum, 11)

    def test_other_values(self):
        other_values = ManyValues()
        other_values.append(22)
        other_values.append(33)
        self.assertEqual(other_values.sum, 55)

    def test_all_values(self):
        single_value = SingleValue(11)
        other_values = ManyValues()
        other_values.append(22)
        other_values.append(33)

        # make a list of all values
        all_values = ManyValues()
        all_values.append(single_value)
        all_values.append(other_values)
        self.assertEqual(all_values.sum, 66)


if __name__ == "__main__":
    unittest.main(exit=False)