from shiny import App

from app.server import app_server
from app.ui import app_ui

app = App(app_ui, app_server)
