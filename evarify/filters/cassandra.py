"""
Filters for Cassandra environment variables.

.. note:: Requires cassandra-driver.
"""

import cassandra


# noinspection PyUnusedLocal
def massage_cassandra_consistency_level(config_val, evar):
    """
    Massage a string value into a reference to a Cassandra driver
    consistency level.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :rtype: int
    :return: A ConsistencyLevel attribute define (as an int).
    :raises: ValueError if the log level is invalid.
    """
    if not config_val:
        raise ValueError(
            "ACLIMA_CASSE_CASSANDRA_CONSISTENCY_LEVEL has an empty value. "
            "Either pass one in, or omit your env var definition to take "
            "the default.")
    config_val = config_val.upper()
    level = getattr(cassandra.ConsistencyLevel, config_val)
    if not level:
        raise ValueError(
            "Invalid value for ACLIMA_CASSE_CASSANDRA_CONSISTENCY_LEVEL: %s",
            config_val
        )
    return level
