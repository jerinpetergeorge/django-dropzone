import typing

from django.conf import settings
from django.utils.module_loading import import_string


class AppSettings:
    def __init__(
        self,
        user_settings: str,
        defaults: dict,
        import_strings: typing.Optional[list] = None,
        merge_dicts: typing.Optional[list] = None,
    ):
        self._user_settings = user_settings
        self.defaults = defaults
        self.import_strings = import_strings or []
        self.merge_dicts = merge_dicts or []

    @property
    def user_settings(self):
        return getattr(settings, self._user_settings, {})

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid setting: '%s'" % attr)  # pragma: no cover

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        if attr in self.merge_dicts:
            _user_dict = self.user_settings.get(attr, {})
            _default_dict = self.defaults[attr]
            val = {**_default_dict, **_user_dict}

        return val


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '{}' for API setting '{}'. {}: {}.".format(
            val,
            setting_name,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg)
