"""
Prophet Model package params
load and validate the environment variables in the `.env`
"""

import os

# Remote or Local path
REMOTE = os.environ.get("REMOTE")

# Load Path
PATH = os.environ.get("PATH")

# Prophet Model params
freq_analysis = os.environ.get("freq_analysis")
LOADED = os.environ.get("LOADED")
SAVED = os.environ.get("SAVED")
PATH_MODELS = os.environ.get("PATH_MODELS")
PATH_DF = os.environ.get("PATH_DF")
