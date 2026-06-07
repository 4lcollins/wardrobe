from pathlib import Path
from jinja2 import Environment, FileSystemLoader

template_dir = Path(__file__).parent.parent / "templates"

env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=True
)

with open(template_dir / "wardrobe.css") as f:
    EMAIL_CSS = f.read()


def render_template(name: str, **kwargs):
    template = env.get_template(name)
    kwargs["css"] = EMAIL_CSS
    return template.render(**kwargs)