from shiny import App

from web.server import app_server
from web.ui import app_ui

app = App(app_ui, app_server)