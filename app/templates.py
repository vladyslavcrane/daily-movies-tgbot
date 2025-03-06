from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())


def get_rendered_template(template_path, context=None):
    if context is None:
        context = {}
    template = env.get_template(template_path)
    return template.render(**context)
