from shiny import App, run_app
from src.ui import app_ui
from src.server import app_server

from src.config import CONFIG

import logging
logging.basicConfig(level=CONFIG.LOG_LEVEL)

app = App(app_ui, app_server)