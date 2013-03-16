"""
Application configuration.
"""

import os.path
from os.path import join

WINTERFELL,ED,AL = range(0,3)
env = WINTERFELL

# General

APP_NAME = "Evelyn"
SCRIPT_EXTENSION = "ev"
#APP_DIR = os.path.expanduser("~/evelyn")
#APP_DIR = "/media/NARSIL/evelyn"
APP_DIR = {
    WINTERFELL: os.path.expanduser("~/evelyn"),
    ED: "/media/NARSIL/evelyn",
    AL: "/media/NARSIL/evelyn",
}[env]
SCREENSHOT_FORMAT = "png"

# API - Video Cache

#CACHE_DIR = "/tmp/diss/videocache"
CACHE_DIR = join(APP_DIR, "videocache")
#FORMAT = "worst"
#FORMAT = "best"
FORMAT = {
    WINTERFELL: "worst",
    ED: "worst",
    AL: "worst",
}[env]

# UI - Graphical Editor

EMPTY_GAP_ANIMATION_INTERVAL = 2000
PALETTE_WIDTH = 350
SCRIPT_EDIT_MIN_WIDTH = 700
PREVIEW_WIDTH = 350
