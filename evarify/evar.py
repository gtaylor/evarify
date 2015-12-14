"""
Pulls config values from environment variables. Checks to make sure we
have everything.
"""
import os
from collections import UserDict


class EnvironmentVariable(object):
    def __init__(self, name, is_required=True, default_val=None,
                 filters=None, help_txt=None):
        self.name = name
        self.is_required = is_required
        self.default_val = default_val
        self.filters = filters or []
        self.help_txt = help_txt


class ConfigStore(UserDict):
    def __init__(self, evar_defs):
        super(ConfigStore, self).__init__()
        self.evar_defs = evar_defs

    def load_values(self):
        """
        Go through the env var map, transferring the values to this object
        as attributes.

        .. note:: The attrib names will match ``config_name``, so be wary
            of collisions.

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
