from pathlib import Path

from shiny import App

from web.server import app_server
from web.ui import app_ui

static_assets = Path(__file__).parent / "web" / "www"

app = App(app_ui, app_server, static_assets=static_assets)
