.. _getting_started:

.. include:: global.txt

Getting Started
===============

This document will walk you through what you need to know in order to get
started with using evarify.

ConfigStore and EnvironmentVariable
-----------------------------------

First, create a new module within your application that will hold your
configuration. We suggest something like ``config.py``.

.. tip:: You'll want to be careful when importing any of your project's other
    modules from within ``config.py`` so you won't run into circular imports.

Here's a good starting point:

.. code-block:: python

    from evarify import ConfigStore, EnvironmentVariable
    from evarify.filters.python_basics import value_to_python_log_level, \
        value_to_bool

    settings = ConfigStore({
        'LOGLEVEL': EnvironmentVariable(
            name='LOGLEVEL',
            help_txt='The desired logging level (DEBUG|INFO|WARN|ERROR).',
            is_required=False,
            default_val='INFO',
            filters=[value_to_python_log_level],
        )
    })

You'll notice that the top-level container is the
:py:class:`ConfigStore <evarify.ConfigStore>` class. This will hold all of your
:py:class:`EnvironmentVariable <evarify.EnvironmentVariable>` definitions,
and eventually your loaded config values. See the API reference for each
of those classes for more details on what the arguments mean.

Loading Config Values from Environment Variables
------------------------------------------------

The next step is to go to the entrypoint module for your project and import
and load our config values:

.. code-block:: python

    from mymodule.config import settings

    settings.load_values()

This causes the magic to happen. We iterate through your
:py:class:`EnvironmentVariable <evarify.EnvironmentVariable>` definitions,
pull the values, run them through the filters, and set the corresponding
dict key in your :py:class:`ConfigStore <evarify.ConfigStore>`. You can
then reference it with the dict API:

.. code-block:: python

    >>> import logging
    >>> from mymodule.config import settings
    >>> settings.load_values()
    >>> assert settings['LOGGING'] == logging.INFO

Filters
-------

An important part of our
:py:class:`EnvironmentVariable <evarify.EnvironmentVariable>` definitions the
``filters`` param. This is a list of filter functions to pass the environment
variable's value through before storing the result in the
:py:class:`ConfigStore <evarify.ConfigStore>`. They fit the following
signature:

.. code-block:: python

    def your_filter(config_val, evar):
        """
        :param str config_val: The env var value.
        :param EnvironmentVariable evar: The EVar object we are validating
            a value for.
        :raises: ValueError if there are any issues with the value.
        """
        # Your logic here. You can modify the config_val before returning.
        return config_val

The environment variable's values will be passed through these filters in
order, so be sure to arrange things accordingly.

You can easily write your own filters, or use any of our built-ins. See the
:py:mod:`evarify.filters.python_basics` API reference for a list.

Gotchas
-------

* If an :py:class:`EnvironmentVariable <evarify.EnvironmentVariable>` has
  been set to ``required=True`` (the default), you *must* define the environment
  variable when running your application (even if it's an empty value).
* If :py:class:`EnvironmentVariable <evarify.EnvironmentVariable>` has been
  set to ``required=False``, failing to define the environment variable will
  result in the ``default_val`` being used. If no ``default_val`` has been
  passed in, we default to ``None``.
