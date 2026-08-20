from pathlib import Path
from shiny import ui

# Locate wardrobe.css relative to this file
css_path = Path(__file__).parent.parent / "src" / "templates" / "wardrobe.css"

# Inline JS to detect OS preference immediately before render
system_theme_js = """
document.addEventListener("DOMContentLoaded", function() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const targetTheme = isDark ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-bs-theme', targetTheme);
    
    const toggle = document.getElementById('theme_mode');
    if (toggle) {
        toggle.value = targetTheme;
    }
});

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    const newTheme = e.matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-bs-theme', newTheme);
});
"""

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.script(system_theme_js)
    ),
    # Inject external stylesheet cleanly
    ui.include_css(css_path) if css_path.exists() else None,
    
    # Header & Dark Mode Toggle
    ui.div(
        ui.div(
            ui.h1("Wardrobe Stylist", class_="hero-header"),
            ui.p(
                "Tailored daily outfit recommendations calibrated to real-time temperature forecasts.",
                class_="sub-header",
            ),
        ),
        ui.input_dark_mode(id="theme_mode", mode="light"),
        class_="d-flex justify-content-between align-items-end mb-3",
    ),
    ui.tags.hr(),
    
    # Main Grid Layout
    ui.layout_columns(
        ui.card(
            ui.card_header("Location"),
            ui.input_text("city", "City", placeholder="e.g. Salt Lake City"),
            ui.input_text("state_abb", "State Abbreviation", placeholder="e.g. UT"),
            ui.input_action_button(
                "run_btn", "Generate Recommendations", class_="btn-primary w-100"
            ),
        ),
        ui.div(
            ui.output_ui("display_output"),
        ),
        col_widths={"sm": (4, 8)},
    ),
)