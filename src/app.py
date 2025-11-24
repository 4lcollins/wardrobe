from shiny import App
from src.ui import app_ui
from src.server import app_server

app = App(app_ui, app_server)