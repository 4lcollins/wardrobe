from shiny import App

from web.ui import app_ui
from web.server import app_server

app = App(app_ui, app_server)