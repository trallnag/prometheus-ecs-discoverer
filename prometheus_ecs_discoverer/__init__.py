import os

from dynaconf import Dynaconf

# Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0


current_directory = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    envvar_prefix="DYNACONF", settings_files=[f"{current_directory}/settings.toml",],
)

settings["DEBUG"] = True if settings.LOG_LEVEL == "DEBUG" else False

s = settings
