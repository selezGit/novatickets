import os

env = os.getenv("ENVIRONMENT", "production")

if env == "dev":
    from .dev import *  # noqa
elif env == "production":
    from .production import *  # noqa
else:
    raise ValueError("Unknown settings")
