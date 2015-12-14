.. _index:

.. include:: global.txt

evarify: Transform and Validate Environment Variables
=====================================================

evarify_ is a `MIT Licensed <MIT License_>`_ Python library that provides some
simple transformations and validators for environment variables.

For example, let's say you are writing a daemon that has an environment
variable, ``SEED_SERVERS`` that expects a comma-separated list of IP addresses.
evarify helps ensure that the value is being passed, that it is in the
expected format, and it will do the conversion to a list for you

.. code-block:: python

   from evarify import ConfigStore, EnvironmentVariable
   from evarify.filters.python_basics import comma_separated_to_set, \
      validate_is_boolean_true

   settings = ConfigStore({
      'SEED_SERVERS': EnvironmentVariable(
          name='SEED_SERVERS',
          filters=[comma_separated_to_set, validate_is_boolean_true],
      ),
   })
   settings.load_values()

   # Assuming our environment variable was ``SEED_SERVERS=192.168.1.50,192.168.1.51``
   >>> settings['SEED_SERVERS']
   ['192.168.1.50', '192.168.1.51']

All functions specified in the ``filters`` keyword are ran in order against
the environment variable's value. In the example above, we were able to
transform the input and validate it quickly and easily.

User Guide
----------

.. toctree::
   :maxdepth: 2

   installation
   getting_started
   api_reference

Community Guide
---------------

.. toctree::
   :maxdepth: 1
   
   support
   release_notes

