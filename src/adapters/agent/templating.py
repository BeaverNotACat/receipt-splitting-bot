from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("src.adapters.agent"), autoescape=select_autoescape()
)

system_prompt_template = env.get_template("system_prompt.jinja")
