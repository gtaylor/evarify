import os
import logging
import unittest

from evarify import ConfigStore, EnvironmentVariable
from evarify.filters.python_basics import value_to_python_log_level, \
    value_to_bool


class ConfigStoreTestCase(unittest.TestCase):
    """
    Put ConfigStore through its paces.
    """

    def setUp(self):
        self.pre_environ = os.environ.copy()

    def tearDown(self):
        os.environ = self.pre_environ.copy()

    def test_empty_store(self):
        """
        Test empty ConfigStore being validated.
        """
        store = ConfigStore({})
        store.load_values()

    def test_simple_load_and_filter(self):
        """
        Tests a simple evar transformation.
        """
        store = ConfigStore({
            'LOGLEVEL': EnvironmentVariable(
                name='LOGLEVEL',
                help_txt='The desired logging level (DEBUG|INFO|WARN|ERROR).',
                is_required=False,
                default_val='INFO',
                filters=[value_to_python_log_level],
            )
        })
        # The filter uppercases this and makes sure it's valid.
        os.environ['LOGLEVEL'] = 'info'
        store.load_values()
        # The end result is a properly formed Python logging level.
        self.assertEqual(store['LOGLEVEL'], logging.INFO)

    def test_simple_load_and_filter_failure(self):
        """
        Tests a single evar with a failing filter.
        """
        store = ConfigStore({
            'LOGLEVEL': EnvironmentVariable(
                name='LOGLEVEL',
                help_txt='The desired logging level (DEBUG|INFO|WARN|ERROR).',
                is_required=False,
                default_val='INFO',
                filters=[value_to_python_log_level],
            )
        })
        # This is an invalid logging level.
        os.environ['LOGLEVEL'] = 'info-YAY'
        self.assertRaises(ValueError, store.load_values)

    def test_unrequired_with_default_values(self):
        """
        Tests an evar that isn't required, but has a default.
        """
        store = ConfigStore({
            'A_BOOL_SETTING': EnvironmentVariable(
                name='BOOL_EVAR',
                is_required=False,
                default_val='true',
                filters=[value_to_bool],
            ),
        })
        store.load_values()
        self.assertTrue(store['A_BOOL_SETTING'])

    def test_unrequired_without_default_values(self):
        """
        Tests an evar that isn't required, and has no default.
        """
        store = ConfigStore({
            'A_BOOL_SETTING': EnvironmentVariable(
                name='BOOL_EVAR',
                is_required=False,
                filters=[value_to_bool],
            ),
        })
        store.load_values()
        # No value was specified in an evar. The default default value is
        # None, which gets filtered to False.
        self.assertEqual(store['A_BOOL_SETTING'], False)

    def test_required_without_default_values(self):
        """
        Tests an evar that is required, but has no default.
        """
        store = ConfigStore({
            'A_BOOL_SETTING': EnvironmentVariable(
                name='BOOL_EVAR',
                is_required=True,
                filters=[value_to_bool],
            ),
        })
        self.assertRaises(RuntimeError, store.load_values)

    def test_required_with_default_values(self):
        """
        Tests an evar that is required and has a default.
        """
        store = ConfigStore({
            'A_BOOL_SETTING': EnvironmentVariable(
                name='BOOL_EVAR',
                is_required=True,
                filters=[value_to_bool],
            ),
        })
        # "Required" means it must be defined (even if the value is empty),
        # so this will still fail.
        self.assertRaises(RuntimeError, store.load_values)
