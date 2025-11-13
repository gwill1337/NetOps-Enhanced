from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_MAP = {
    "cisco": "cisco.j2",
    "ios": "cisco.j2",
    "juniper": "juniper.j2",
    "junos": "juniper.j2",
    "paloalto": "paloalto.j2",
    "panos": "paloalto.j2"
}

def render_config(data):
    os_type = data.get("os", "").lower()
    if not os_type:
        raise ValueError(f"Device {data.get('hostname')} dont have 'os' field")

    if os_type not in TEMPLATE_MAP:
        raise ValueError(f"OS '{os_type}' not support")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template(TEMPLATE_MAP[os_type])
    return template.render(**data)
