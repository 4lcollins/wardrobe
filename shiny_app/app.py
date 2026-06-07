from shiny import App

from shiny_app.server import app_server
from shiny_app.ui import app_ui

app = App(app_ui, app_server)
