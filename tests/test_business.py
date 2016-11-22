# _*_ coding: utf-8 _*_
import unittest
import pickle
from unittest.mock import patch, MagicMock
from api.business import *


class TestBusiness(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOne(self):
        self.assertEqual(1, 1, "One equals one")

    def test_no_diff(self):
        # test data
        right_data = pickle.dumps({'ola': 'mundo'})
        left_data = pickle.dumps({'ola': 'mundo'})
        expected_result = {'equal': True, 'same_size': True, 'diffs': []}

        diff = Diff()
        # Mocking data
        diff.right.get = MagicMock(return_value=right_data)
        diff.left.get = MagicMock(return_value=left_data)

        self.assertEqual(diff.getDiff(), expected_result)

    def test_different_size(self):
        # test data
        right_data = pickle.dumps({'ola': 'mundo'})
        left_data = pickle.dumps({'ola': 'mundo123'})
        expected_result = {'equal': False, 'same_size': False, 'diffs': []}

        diff = Diff()
        # Mocking data
        diff.right.get = MagicMock(return_value=right_data)
        diff.left.get = MagicMock(return_value=left_data)

        self.assertEqual(diff.getDiff(), expected_result)

    def test_different_same_size(self):
        # test data
        right_data = pickle.dumps({'ola': 'mundo123'})
        left_data = pickle.dumps({'ola': 'mundo456'})
        expected_result = {
            'equal': False,
            'same_size': True,
            'diffs': [
                [14, 3]
            ]
        }

        diff = Diff()
        # Mocking data
        diff.right.get = MagicMock(return_value=right_data)
        diff.left.get = MagicMock(return_value=left_data)

        self.assertEqual(diff.getDiff(), expected_result)

    def test_different_same_size_more_than_one_diff(self):
        # teste data
        right_data = pickle.dumps({'ola12': 'mundo123'})
        left_data = pickle.dumps({'ola34': 'mundo456'})
        expected_result = {
            'equal': False,
            'same_size': True,
            'diffs': [
                [5, 2],
                [16, 3]
            ]
        }

        diff = Diff()
        diff.right.get = MagicMock(return_value=right_data)
        diff.left.get = MagicMock(return_value=left_data)

        self.assertEqual(diff.getDiff(), expected_result)
