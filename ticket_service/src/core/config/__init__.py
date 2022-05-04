import os

env = os.getenv("ENVIRONMENT", "production")

if env == "dev":
    # try:
    # from .local import *  # noqa
    # except ImportError:
    from .dev import *  # noqa
elif env == "production":
    from .production import *  # noqa
else:
    raise ValueError("Unknown settings")
