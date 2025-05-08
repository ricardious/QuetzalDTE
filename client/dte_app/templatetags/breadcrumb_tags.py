from django import template

register = template.Library()

@register.inclusion_tag('components/molecules/breadcrumbs.html')
def breadcrumbs(*args):
    items = []
    for url, text in zip(args[0::2], args[1::2]):
        items.append({
            'url': url,
            'text': text,
        })
    return {'items': items}

@register.inclusion_tag('components/organisms/page_header.html')
def page_header(*args, title, description=None):
    items = []
    for i in range(0, len(args), 2):
        url  = args[i]
        text = args[i+1]
        items.append({'url': url, 'text': text})
    return {
        'breadcrumb_items': items,
        'title': title,
        'description': description,
    }