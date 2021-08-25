import os

from dynaconf import Dynaconf  # type: ignore


current_directory = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    envvar_prefix="PROMED",
    settings_files=[
        f"{current_directory}/settings.toml",
    ],
)

settings["DEBUG"] = True if settings.LOG_LEVEL == "DEBUG" else False

s = settings
