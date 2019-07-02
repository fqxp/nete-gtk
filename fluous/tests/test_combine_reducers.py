from unittest.mock import Mock
from fluous.functions import combine_reducers
from pyrsistent import freeze
import unittest


class CombineReducersTestCase(unittest.TestCase):

    def test_returns_a_function_that_combines_results_of_multiple_reducers(self):
        foo_reducer_mock = Mock()
        foo_reducer_mock.configure_mock(return_value=freeze({'bar': 'BAR-STATE-AFTER'}))
        what_reducer_mock = Mock()
        what_reducer_mock.configure_mock(return_value=freeze({'ever': 'EVER-STATE-AFTER'}))
        state = freeze({
            'foo': {'bar': 'bar-state-before'},
            'what': {'ever': 'ever-state-before'},
        })

        reducer = combine_reducers({
            'foo': foo_reducer_mock,
            'what': what_reducer_mock,
        })
        new_state = reducer(state, 'SOME-ACTION')

        foo_reducer_mock.assert_called_with(freeze({'bar': 'bar-state-before'}), 'SOME-ACTION')
        what_reducer_mock.assert_called_with(freeze({'ever': 'ever-state-before'}), 'SOME-ACTION')
        self.assertEqual(new_state, freeze({
            'foo': {'bar': 'BAR-STATE-AFTER'},
            'what': {'ever': 'EVER-STATE-AFTER'},
        }))
