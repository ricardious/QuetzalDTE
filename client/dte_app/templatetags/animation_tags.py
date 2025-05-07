from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def anim_player(url=None, filepath=None, height=None, width=None, speed=1.0, loop=True, autoplay=True, controls=False, background="transparent"):
    
    filepath = static(filepath)
    
    loop_attr = "loop" if loop else ""
    autoplay_attr = "autoplay" if autoplay else ""
    controls_attr = "controls" if controls else ""
    
    style_parts = []
    if width:
        style_parts.append(f"width: {width};")
    if height:
        style_parts.append(f"height: {height};")
        
    if not style_parts:
        style_parts = ["width: 100%;", "height: auto;", "max-width: 100%;"]
    
    style_attr = f'style="{" ".join(style_parts)}"'
    
    player_tag = f"""
    <lottie-player
        src="{url if url else filepath}"
        background="{background}"
        speed="{speed}"
        {style_attr}
        {loop_attr}
        {autoplay_attr}
        {controls_attr}>
    </lottie-player>
    """
    return mark_safe(player_tag)