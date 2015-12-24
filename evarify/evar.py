"""
Pulls config values from environment variables. Checks to make sure we
have everything.
"""
import os


class ConfigStore(dict):
    """
    This is the container for your :py:class:`EnvironmentVariable` definitions,
    along with their eventual loaded config values. Once :py:meth:`load_values`
    is ran on an instance of this class, the config values are addressable
    via the Python dict API.
    """
    def __init__(self, evar_defs):
        """
        :param dict evar_defs: Pass in a dict whose keys are config
            names and the values are :py:class:`EnvironmentVariable`
            instances.
        """
        self.evar_defs = evar_defs

    def load_values(self):
        """
        Go through the env var map, transferring the values to this object
        as attributes.

        :raises: RuntimeError if a required env var isn't defined.
        """

        for config_name, evar in self.evar_defs.items():
            if evar.is_required and evar.name not in os.environ:
                raise RuntimeError((
                    "Missing required environment variable: {evar_name}\n"
                    "{help_txt}"
                ).format(evar_name=evar.name, help_txt=evar.help_txt))
            # Env var is present. Transfer its value over.
            if evar.name in os.environ:
                self[config_name] = os.environ.get(evar.name)
            else:
                self[config_name] = evar.default_val
            # Perform any validations or transformations.
            for filter in evar.filters:
                current_val = self.get(config_name)
                new_val = filter(current_val, evar)
                self[config_name] = new_val
        # This is the top-level filter that is often useful for checking
        # the values of related env vars (instead of individual validation).
        self._filter_all()

    def _filter_all(self):
        """
        This runs after all individual env vars have been loaded.
        Feel free to modify values or raise exceptions as need be.

        :raises: ValueError if something is amiss.
        """
        pass


class EnvironmentVariable(object):
    """
    Defines an Environment Variable to handle.
    """
    def __init__(self, name, is_required=True, default_val=None,
                 filters=None, help_txt=None):
        """
        :param str name: The name of the environment variable. *This is
            case-sensitive!*
        :keyword bool is_required: If ``True``, this variable must be defined
            when your Python process starts. If ``False``, the default loaded
            value will match ``default_val``.
        :keyword default_val: If ``is_required`` is ``False`` and this
            environment variable is not defined, this value will be loaded.
        :keyword list filters: A list of functions to pass the environment
            variable's value (or default value) through. Order is
            significant!
        :keyword str help_txt: Optional help text describing the environment
            variable.
        """
        self.name = name
        self.is_required = is_required
        self.default_val = default_val
        self.filters = filters or []
        self.help_txt = help_txt
