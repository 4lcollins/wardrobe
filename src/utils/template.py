from pathlib import Path

from jinja2 import Environment, FileSystemLoader

root_dir = Path(__file__).resolve().parent.parent.parent
theme_css_path = root_dir / "web" / "www" / "theme.css"

env = Environment(
    loader=FileSystemLoader(root_dir),
    autoescape=True,
)


def render_template(name: str, use_email_css: bool = False, **kwargs):
    if use_email_css:
        kwargs["css"] = theme_css_path.read_text(encoding="utf-8")

    template = env.get_template(name)
    return template.render(**kwargs)