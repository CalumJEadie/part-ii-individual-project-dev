"""
Application configuration.
"""

import os.path
from os.path import join

# General

APP_NAME = "Evelyn"
SCRIPT_EXTENSION = "ev"
APP_DIR = os.path.expanduser("~/evelyn")
SCREENSHOT_FORMAT = "png"

# API - Video Cache

#CACHE_DIR = "/tmp/diss/videocache"
CACHE_DIR = join(APP_DIR, "videocache")
config.FORMAT = "worst"
# config.FORMAT = "best"

# UI - Graphical Editor

EMPTY_GAP_ANIMATION_INTERVAL = 2000
PALETTE_WIDTH = 350
SCRIPT_EDIT_MIN_WIDTH = 700
PREVIEW_WIDTH = 350