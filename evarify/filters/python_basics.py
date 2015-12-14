import logging


# noinspection PyUnusedLocal
def comma_separated_str_to_list(config_val, evar):
    """
    Splits a comma-separated environment variable into a list of strings.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :rtype: list
    :return: The equivalent list for a comma-separated string.
    """
    if not config_val:
        return []
    return [token.strip() for token in config_val.split(',')]


# noinspection PyUnusedLocal
def comma_separated_to_set(config_val, evar):
    """
    Splits a comma-separated environment variable into a set of strings.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :rtype: set
    :return: The equivalent set for a comma-separated string.
    """
    return set(comma_separated_str_to_list(config_val, evar))


# noinspection PyUnusedLocal
def value_to_none(config_val, evar):
    """
    Given a value that evaluates to a boolean False, return None.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :rtype: str or None
    :return: Either the non-False value or None.
    """
    if not config_val:
        return None
    return config_val


# noinspection PyUnusedLocal
def value_to_int(config_val, evar):
    """
    Convert the value to int.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :rtype: int
    """
    return int(config_val)


# noinspection PyUnusedLocal
def value_to_bool(config_val, evar):
    """
    Massages the 'true' and 'false' strings to bool equivalents.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :rtype: bool
    :return: True or False, depending on the value.
    """
    if not config_val:
        return False
    if config_val.strip().lower() == 'true':
        return True
    else:
        return False


# noinspection PyUnusedLocal
def validate_is_not_none(config_val, evar):
    """
    If the value is ``None``, fail validation.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :raises: ValueError if the config value is None.
    """
    if config_val is None:
        raise ValueError(
            "Value for environment variable '{evar_name}' can't "
            "be empty.".format(evar_name=evar.name))
    return config_val


# noinspection PyUnusedLocal
def validate_is_boolean_true(config_val, evar):
    """
    Make sure the value evaluates to boolean True.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :raises: ValueError if the config value evaluates to boolean False.
    """
    if config_val is None:
        raise ValueError(
            "Value for environment variable '{evar_name}' can't "
            "be empty.".format(evar_name=evar.name))
    return config_val


# noinspection PyUnusedLocal
def value_to_python_log_level(config_val, evar):
    """
    Convert an evar value into a Python logging level constant.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :return: A validated string.
    :raises: ValueError if the log level is invalid.
    """
    if not config_val:
        config_val = evar.default_val
    config_val = config_val.upper()
    # noinspection PyProtectedMember
    return logging._checkLevel(config_val)
