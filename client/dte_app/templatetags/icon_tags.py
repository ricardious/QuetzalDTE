from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from pathlib import Path

register = template.Library()

@register.simple_tag
def icon(icon_id, classes=""):
    url = static("assets/icons/sprite.svg")
    svg = (
        f'<svg class="{classes}" aria-hidden="true" focusable="false">'
        f'  <use href="{url}#{icon_id}"></use>'
        f'</svg>'
    )
    return mark_safe(svg)

@register.simple_tag
def svg(path, classes=""):
    url = static(path)
    svg_code = Path(url[1:]).read_text()
    if classes:
        svg_code = svg_code.replace(
            "<svg", f'<svg class="{classes}"', 1
        )
    return mark_safe(svg_code)
